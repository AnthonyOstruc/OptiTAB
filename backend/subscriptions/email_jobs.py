import logging
import threading
import time

from django.contrib.auth import get_user_model
from django.db import close_old_connections, transaction

from .models import PaymentHistory, UserSubscription
from core.services import EmailService
from .stripe_services import _hydrate_payment_history_invoice

logger = logging.getLogger(__name__)
User = get_user_model()

# Configuration retry
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

# Anti-doublon in-process
_scheduled_subscription_email_jobs = set()
_scheduled_subscription_email_jobs_lock = threading.Lock()
_scheduled_invoice_email_jobs = set()
_scheduled_invoice_email_jobs_lock = threading.Lock()
_scheduled_cancellation_email_jobs = set()
_scheduled_cancellation_email_jobs_lock = threading.Lock()


def _parse_gift_metadata(metadata):
    """Parse les métadonnées pour extraire les infos de cadeau."""
    safe_metadata = metadata if isinstance(metadata, dict) else {}
    is_gift = str(safe_metadata.get('is_gift') or '').lower() == 'true'
    payer_user_id = safe_metadata.get('payer_user_id')
    payer = None
    if is_gift and payer_user_id:
        try:
            payer = User.objects.get(id=payer_user_id)
        except User.DoesNotExist:
            payer = None
    return is_gift, payer


def _check_payment_history_sent(payment_history_id, job_name="Email job"):
    """Vérifie si l'email a déjà été envoyé. Retourne (payment_history, should_continue)."""
    try:
        payment_history = PaymentHistory.objects.select_related('user').get(pk=payment_history_id)
        if payment_history.email_sent:
            return payment_history, False
        return payment_history, True
    except PaymentHistory.DoesNotExist:
        logger.warning("%s: PaymentHistory %s introuvable", job_name, payment_history_id)
        return None, False


def _retry_with_delay(retry_count, job_name, context_msg, retry_fn):
    """Gère la logique de retry avec délai."""
    if retry_count < MAX_RETRIES:
        logger.info(
            "%s: %s, retry %d/%d dans %ds",
            job_name,
            context_msg,
            retry_count + 1,
            MAX_RETRIES,
            RETRY_DELAY_SECONDS,
        )
        time.sleep(RETRY_DELAY_SECONDS)
        close_old_connections()
        return retry_fn()
    logger.warning("%s: %s après %d tentatives", job_name, context_msg, MAX_RETRIES)
    return None


def _schedule_unique_job(key, scheduled_set, lock, job_fn):
    """Exécute `job_fn` une seule fois par `key` (anti-doublon in-process)."""
    with lock:
        if key in scheduled_set:
            return False
        scheduled_set.add(key)

    try:
        job_fn()
    finally:
        with lock:
            scheduled_set.discard(key)
    return True


# =============================================================================
# JOB: Emails d'abonnement (nouvel abonné)
# =============================================================================

def _send_subscription_emails_job(payment_history_id, stripe_subscription_id, metadata=None, retry_count=0):
    """Envoie (une seule fois) les emails liés à une souscription payée."""
    close_old_connections()

    # Vérification préalable (hors transaction)
    payment_history_check, should_continue = _check_payment_history_sent(payment_history_id, "Email job")
    if not should_continue:
        return

    # Vérifier si l'abonnement existe
    user_subscription = (
        UserSubscription.objects
        .select_related('user', 'plan', 'niveau_pays', 'niveau_pays__pays')
        .filter(stripe_subscription_id=stripe_subscription_id)
        .first()
    )

    if not user_subscription:
        return _retry_with_delay(
            retry_count,
            "Email job",
            f"abonnement local introuvable (stripe_subscription_id={stripe_subscription_id})",
            lambda: _send_subscription_emails_job(
                payment_history_id, stripe_subscription_id, metadata, retry_count + 1
            )
        )

    try:
        with transaction.atomic():
            payment_history = (
                PaymentHistory.objects
                .select_for_update()
                .select_related('user')
                .get(pk=payment_history_id)
            )
            if payment_history.email_sent:
                return

            pdf_url, hosted_url = _hydrate_payment_history_invoice(payment_history)
            invoice_link = (pdf_url or hosted_url or '').strip() or None

            is_gift, payer = _parse_gift_metadata(metadata)

            if is_gift and payer:
                EmailService.send_gift_subscription_notification(
                    recipient=user_subscription.user,
                    gifter=payer,
                    plan=user_subscription.plan,
                    niveau=user_subscription.niveau_pays,
                )
                EmailService.send_gift_purchase_confirmation(
                    payer=payer,
                    recipient=user_subscription.user,
                    plan=user_subscription.plan,
                    niveau=user_subscription.niveau_pays,
                    is_pass=False,
                    invoice_link=invoice_link,
                )
            else:
                EmailService.send_subscription_confirmation(
                    user_subscription.user,
                    user_subscription.plan,
                    user_subscription.niveau_pays,
                    invoice_link=invoice_link,
                )

            EmailService.send_new_subscription_notification_to_admin(
                user=user_subscription.user,
                plan=user_subscription.plan,
                niveau=user_subscription.niveau_pays,
                is_gift=is_gift,
                payer=payer,
            )

            payment_history.email_sent = True
            payment_history.save(update_fields=['email_sent'])
    except PaymentHistory.DoesNotExist:
        logger.warning("Email job: PaymentHistory %s introuvable", payment_history_id)
    except Exception as exc:
        logger.error("Email job: erreur lors de l'envoi (payment_history_id=%s): %s", payment_history_id, exc)


def _schedule_subscription_emails(payment_history_id, stripe_subscription_id, metadata=None):
    """Programme l'envoi des emails d'abonnement (anti-doublon)."""
    scheduled = _schedule_unique_job(
        key=payment_history_id,
        scheduled_set=_scheduled_subscription_email_jobs,
        lock=_scheduled_subscription_email_jobs_lock,
        job_fn=lambda: _send_subscription_emails_job(payment_history_id, stripe_subscription_id, metadata),
    )
    if scheduled:
        logger.info(
            "Emails d'abonnement envoyés (payment_history_id=%s, stripe_subscription_id=%s)",
            payment_history_id,
            stripe_subscription_id,
        )


# =============================================================================
# JOB: Email de facture (renouvellement)
# =============================================================================

def _send_invoice_email_job(payment_history_id, stripe_subscription_id, metadata=None, retry_count=0):
    """Envoie (une seule fois) l'email de facture pour une échéance d'abonnement payée."""
    close_old_connections()

    # Vérification préalable (hors transaction)
    payment_history_check, should_continue = _check_payment_history_sent(payment_history_id, "Invoice email job")
    if not should_continue:
        return

    # Récupérer l'URL de facture
    pdf_url, hosted_url = _hydrate_payment_history_invoice(payment_history_check)
    invoice_link = (pdf_url or hosted_url or '').strip()

    if not invoice_link:
        return _retry_with_delay(
            retry_count,
            "Invoice email job",
            f"lien de facture indisponible (payment_history_id={payment_history_id})",
            lambda: _send_invoice_email_job(
                payment_history_id, stripe_subscription_id, metadata, retry_count + 1
            )
        )

    try:
        with transaction.atomic():
            payment_history = (
                PaymentHistory.objects
                .select_for_update()
                .select_related('user')
                .get(pk=payment_history_id)
            )
            if payment_history.email_sent:
                return

            is_gift, payer = _parse_gift_metadata(metadata)
            recipient = payer if (is_gift and payer) else payment_history.user

            EmailService.send_invoice_receipt(recipient, payment_history, invoice_link)

            payment_history.email_sent = True
            payment_history.save(update_fields=['email_sent'])
    except PaymentHistory.DoesNotExist:
        logger.warning("Invoice email job: PaymentHistory %s introuvable", payment_history_id)
    except Exception as exc:
        logger.error("Invoice email job: erreur lors de l'envoi (payment_history_id=%s): %s", payment_history_id, exc)


def _schedule_invoice_email(payment_history_id, stripe_subscription_id, metadata=None):
    """Programme l'envoi de l'email de facture (anti-doublon)."""
    scheduled = _schedule_unique_job(
        key=payment_history_id,
        scheduled_set=_scheduled_invoice_email_jobs,
        lock=_scheduled_invoice_email_jobs_lock,
        job_fn=lambda: _send_invoice_email_job(payment_history_id, stripe_subscription_id, metadata),
    )
    if scheduled:
        logger.info(
            "Email facture envoyé (payment_history_id=%s, stripe_subscription_id=%s)",
            payment_history_id,
            stripe_subscription_id,
        )


# =============================================================================
# JOB: Emails de résiliation
# =============================================================================

def _send_cancellation_emails_job(user_subscription_id, cancel_type='scheduled', stripe_subscription_id=None, metadata=None):
    """Envoie les emails liés à une résiliation (utilisateur + admin)."""
    close_old_connections()
    cancel_type = (cancel_type or '').strip().lower() or 'scheduled'
    is_scheduled = cancel_type == 'scheduled'

    try:
        user_subscription = (
            UserSubscription.objects
            .select_related('user', 'plan', 'niveau_pays', 'niveau_pays__pays')
            .get(pk=user_subscription_id)
        )

        logger.info(
            "Cancellation email job: envoi pour user_subscription_id=%s, cancel_type=%s, status=%s, cancel_at_period_end=%s",
            user_subscription_id,
            cancel_type,
            user_subscription.status,
            user_subscription.cancel_at_period_end,
        )

        is_gift, payer = _parse_gift_metadata(metadata)
        
        if is_gift and payer:
            recipient = payer
            beneficiary = user_subscription.user
        else:
            recipient = user_subscription.user
            beneficiary = None

        # Envoyer email à l'utilisateur
        user_email_sent = EmailService.send_subscription_cancellation_confirmation(
            user=recipient,
            plan=user_subscription.plan,
            niveau=user_subscription.niveau_pays,
            effective_end=user_subscription.current_period_end,
            is_scheduled=is_scheduled,
            beneficiary=beneficiary,
        )
        logger.info("Cancellation email to user: %s (sent=%s)", recipient.email, user_email_sent)

        # Envoyer email à l'admin
        admin_email_sent = EmailService.send_subscription_cancellation_notification_to_admin(
            user=recipient,
            plan=user_subscription.plan,
            niveau=user_subscription.niveau_pays,
            effective_end=user_subscription.current_period_end,
            is_scheduled=is_scheduled,
            beneficiary=beneficiary,
        )
        logger.info("Cancellation email to admin: sent=%s", admin_email_sent)

    except UserSubscription.DoesNotExist:
        logger.warning(
            "Cancellation email job: abonnement introuvable (user_subscription_id=%s)",
            user_subscription_id,
        )
    except Exception as exc:
        logger.error(
            "Cancellation email job: erreur lors de l'envoi (user_subscription_id=%s): %s",
            user_subscription_id,
            exc,
            exc_info=True,
        )


def _schedule_cancellation_emails(user_subscription_id, cancel_type='scheduled', stripe_subscription_id=None, metadata=None):
    """Programme l'envoi des emails de résiliation (anti-doublon)."""
    key = f"{user_subscription_id}:{(cancel_type or '').strip().lower()}"
    scheduled = _schedule_unique_job(
        key=key,
        scheduled_set=_scheduled_cancellation_email_jobs,
        lock=_scheduled_cancellation_email_jobs_lock,
        job_fn=lambda: _send_cancellation_emails_job(user_subscription_id, cancel_type, stripe_subscription_id, metadata),
    )
    if scheduled:
        logger.info(
            "Emails résiliation envoyés (user_subscription_id=%s, type=%s)",
            user_subscription_id,
            cancel_type,
        )


__all__ = [
    '_schedule_subscription_emails',
    '_schedule_invoice_email',
    '_schedule_cancellation_emails',
]
