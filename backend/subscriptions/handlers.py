import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from .models import SubscriptionPlan, UserSubscription, PaymentHistory, AccessPass
from pays.models import Niveau
from core.services import EmailService
from .stripe_client import stripe, stripe_error
from .helpers import (
    _append_level_to_description,
    _extract_invoice_period,
    _format_level_label_from_obj,
    _from_timestamp,
    _level_label_from_metadata,
    _resolve_access_days,
    _resolve_plan_mode,
    _stripe_obj_to_dict,
    _sync_user_niveau,
)
from .stripe_services import (
    STRIPE_INVOICE_CUSTOM_FIELDS_MAX,
    _clear_customer_temp_invoice_custom_fields,
    _merge_stripe_custom_fields,
)
from .email_jobs import (
    _schedule_cancellation_emails,
    _schedule_invoice_email,
    _schedule_subscription_emails,
)

logger = logging.getLogger(__name__)
User = get_user_model()


# =============================================================================
# Helpers internes DRY
# =============================================================================

def _get_niveau_from_id(niveau_id):
    """Récupère un niveau actif par son ID, retourne None si non trouvé."""
    if not niveau_id:
        return None
    try:
        return Niveau.objects.get(id=niveau_id, est_actif=True)
    except Niveau.DoesNotExist:
        return None


def _build_subscription_defaults(user, plan, subscription_data, niveau_obj=None, customer_id=None):
    """Construit les defaults pour créer/mettre à jour un UserSubscription."""
    return {
        'user': user,
        'plan': plan,
        'stripe_customer_id': customer_id or subscription_data.get('customer'),
        'status': subscription_data.get('status', 'active'),
        'current_period_start': _from_timestamp(subscription_data.get('current_period_start')),
        'current_period_end': _from_timestamp(subscription_data.get('current_period_end')),
        'trial_end': _from_timestamp(subscription_data.get('trial_end')),
        'cancel_at_period_end': bool(subscription_data.get('cancel_at_period_end')),
        'niveau_pays': niveau_obj,
    }


def _update_subscription_from_stripe(user_subscription, subscription_data, niveau_obj=None):
    """Met à jour un UserSubscription depuis les données Stripe."""
    user_subscription.status = subscription_data.get('status', user_subscription.status)
    user_subscription.current_period_start = _from_timestamp(subscription_data.get('current_period_start'))
    user_subscription.current_period_end = _from_timestamp(subscription_data.get('current_period_end'))
    user_subscription.trial_end = _from_timestamp(subscription_data.get('trial_end'))
    user_subscription.cancel_at_period_end = bool(subscription_data.get('cancel_at_period_end'))
    
    customer_id = subscription_data.get('customer')
    if customer_id:
        user_subscription.stripe_customer_id = customer_id
    
    if niveau_obj:
        user_subscription.niveau_pays = niveau_obj
    
    user_subscription.save()


def _parse_gift_metadata(metadata):
    """Parse les métadonnées pour extraire les infos de cadeau."""
    is_gift = str(metadata.get('is_gift') or '').lower() == 'true'
    payer_user_id = metadata.get('payer_user_id')
    payer = None
    if is_gift and payer_user_id:
        try:
            payer = User.objects.get(id=payer_user_id)
        except User.DoesNotExist:
            payer = None
    return is_gift, payer


# =============================================================================
# Handler: invoice.created
# =============================================================================

def handle_invoice_created(invoice):
    """Ajoute des informations (classe/niveau, bénéficiaire) sur la facture Stripe."""
    try:
        invoice_id = invoice.get('id')
        if not invoice_id:
            return

        # Les champs sont modifiables uniquement tant que la facture est en brouillon
        if invoice.get('status') and invoice.get('status') != 'draft':
            logger.info(
                "invoice.created: %s déjà finalisée (status=%s)",
                invoice_id,
                invoice.get('status'),
            )
            return

        subscription_id = invoice.get('subscription')
        if isinstance(subscription_id, dict):
            subscription_id = subscription_id.get('id')
        if not subscription_id:
            return

        # Récupérer les metadata (priorité: subscription_details -> invoice.metadata -> subscription.metadata)
        metadata = _collect_invoice_metadata(invoice, subscription_id)
        if not metadata:
            return

        # Récupérer le label du niveau
        niveau_label = _get_niveau_label_for_invoice(subscription_id, metadata)
        
        is_gift = str(metadata.get('is_gift') or '').lower() == 'true'
        beneficiary_email = (metadata.get('beneficiary_email') or '').strip()

        if not niveau_label and not (is_gift and beneficiary_email):
            return

        # Ajouter les champs personnalisés à la facture
        _add_custom_fields_to_invoice(invoice, invoice_id, niveau_label, is_gift, beneficiary_email)

    except Exception as exc:
        logger.warning("handle_invoice_created: erreur (%s): %s", invoice.get('id'), exc)


def _collect_invoice_metadata(invoice, subscription_id):
    """Collecte les metadata depuis plusieurs sources."""
    metadata = {}
    
    # subscription_details
    subscription_details = invoice.get('subscription_details') or {}
    if isinstance(subscription_details, dict):
        sub_meta = subscription_details.get('metadata') or {}
        if isinstance(sub_meta, dict):
            metadata.update(sub_meta)
    
    # invoice.metadata
    inv_meta = invoice.get('metadata') or {}
    if isinstance(inv_meta, dict):
        metadata.update(inv_meta)

    # Fallback: récupérer depuis Stripe
    if not metadata and subscription_id:
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription_data = _stripe_obj_to_dict(subscription)
        metadata = subscription_data.get('metadata') or {}

    return metadata if isinstance(metadata, dict) else {}


def _get_niveau_label_for_invoice(subscription_id, metadata):
    """Récupère le label du niveau pour une facture."""
    niveau_label = ''
    try:
        local_sub = (
            UserSubscription.objects
            .select_related('niveau_pays', 'niveau_pays__pays')
            .filter(stripe_subscription_id=subscription_id)
            .first()
        )
        if local_sub and local_sub.niveau_pays:
            niveau_label = _format_level_label_from_obj(local_sub.niveau_pays)
    except Exception:
        pass

    if not niveau_label:
        niveau_label = (_level_label_from_metadata(metadata) or '').strip()

    return niveau_label


def _add_custom_fields_to_invoice(invoice, invoice_id, niveau_label, is_gift, beneficiary_email):
    """Ajoute les champs personnalisés à la facture Stripe."""
    existing_fields = invoice.get('custom_fields') or []
    if not isinstance(existing_fields, list):
        existing_fields = []

    requested_fields = []
    if niveau_label:
        requested_fields.append(('Niveau', niveau_label))
    if is_gift and beneficiary_email:
        requested_fields.append(('Bénéficiaire', beneficiary_email))

    existing_names = {
        str(f.get('name') or '').strip()
        for f in existing_fields
        if isinstance(f, dict)
    }
    requested_names = {name for name, _ in requested_fields}

    # Si déjà 4 champs et aucun de nos champs n'existe → fallback footer
    if len(existing_names) >= STRIPE_INVOICE_CUSTOM_FIELDS_MAX and not (existing_names & requested_names):
        footer_lines = []
        if niveau_label:
            footer_lines.append(f"Niveau : {niveau_label}")
        if is_gift and beneficiary_email:
            footer_lines.append(f"Bénéficiaire : {beneficiary_email}")

        if footer_lines:
            current_footer = (invoice.get('footer') or '').strip()
            appendix = "\n".join(footer_lines)
            if appendix not in current_footer:
                new_footer = (current_footer + "\n" if current_footer else "") + appendix
                stripe.Invoice.modify(invoice_id, footer=new_footer[:500])
        return

    merged_fields = _merge_stripe_custom_fields(existing_fields, requested_fields)
    if merged_fields != existing_fields:
        stripe.Invoice.modify(invoice_id, custom_fields=merged_fields)


# =============================================================================
# Handler: checkout.session.completed (subscription)
# =============================================================================

def handle_checkout_session_completed(session):
    """Gérer la completion d'une session de checkout (abonnement)."""
    customer_id = session.get('customer')
    should_clear_customer_fields = False
    
    try:
        # Vérifier que la session est bien payée
        if not _is_session_paid(session):
            logger.info(f"Session {session.get('id')} ignorée: non payée")
            return

        should_clear_customer_fields = True

        metadata = session.get('metadata') or {}
        user_id = metadata.get('user_id')
        plan_id = metadata.get('plan_id')
        niveau_id = metadata.get('niveau_pays_id')

        if not user_id or not plan_id:
            logger.error("Session checkout sans metadata user/plan (%s)", session.get('id'))
            return

        user = User.objects.get(id=user_id)
        plan = SubscriptionPlan.objects.get(id=plan_id)
        niveau_obj = _get_niveau_from_id(niveau_id)

        # Récupérer l'abonnement Stripe
        subscription = stripe.Subscription.retrieve(session['subscription'])
        subscription_data = _stripe_obj_to_dict(subscription)
        stripe_subscription_id = subscription_data.get('id')

        # Créer ou mettre à jour l'abonnement local
        defaults = _build_subscription_defaults(
            user, plan, subscription_data, niveau_obj, session.get('customer')
        )
        user_subscription, created = UserSubscription.objects.get_or_create(
            stripe_subscription_id=stripe_subscription_id,
            defaults=defaults
        )

        if not created:
            _update_subscription_from_stripe(user_subscription, subscription_data, niveau_obj)
        elif niveau_obj and user_subscription.niveau_pays_id != niveau_obj.id:
            user_subscription.niveau_pays = niveau_obj
            user_subscription.save(update_fields=['niveau_pays'])

        if niveau_obj:
            _sync_user_niveau(user, niveau_obj)

        # Fallback: déclencher l'envoi des emails si la facture est déjà payée
        _ensure_paid_invoice_email_from_session(session)

    except Exception as e:
        logger.error(f"Erreur dans handle_checkout_session_completed: {e}")
    finally:
        if should_clear_customer_fields:
            _clear_customer_temp_invoice_custom_fields(customer_id)


def _is_session_paid(session):
    """Vérifie si une session de checkout est payée."""
    return (
        session.get('status') == 'complete' and
        session.get('payment_status') in ('paid', 'no_payment_required')
    )


def _ensure_paid_invoice_email_from_session(session):
    """Fallback: déclencher l'envoi des emails si la dernière facture est déjà payée."""
    subscription_id = session.get('subscription')
    if not subscription_id:
        return
    
    try:
        subscription = stripe.Subscription.retrieve(subscription_id, expand=['latest_invoice'])
        subscription_data = _stripe_obj_to_dict(subscription)
        latest_invoice = subscription_data.get('latest_invoice')
        
        if not latest_invoice:
            return
            
        if isinstance(latest_invoice, str):
            invoice = _stripe_obj_to_dict(stripe.Invoice.retrieve(latest_invoice))
        else:
            invoice = _stripe_obj_to_dict(latest_invoice)

        if invoice and (invoice.get('paid') or invoice.get('status') == 'paid'):
            handle_payment_succeeded(invoice)
            
    except stripe_error.StripeError as exc:
        logger.warning("Fallback email: erreur Stripe (subscription=%s): %s", subscription_id, exc)
    except Exception as exc:
        logger.warning("Fallback email: erreur (subscription=%s): %s", subscription_id, exc)


# =============================================================================
# Handler: checkout.session.completed (one-time payment)
# =============================================================================

def handle_checkout_session_payment_completed(session):
    """Gérer la completion d'une session de checkout en mode paiement unique."""
    try:
        if not _is_session_paid(session):
            logger.info(f"Session paiement {session.get('id')} ignorée: non payée")
            return

        metadata = session.get('metadata') or {}
        user_id = metadata.get('user_id')
        plan_id = metadata.get('plan_id')
        plan_mode = metadata.get('plan_mode')
        niveau_id = metadata.get('niveau_pays_id')

        if not user_id or not plan_id:
            logger.error("Session checkout paiement sans user/plan (%s)", session.get('id'))
            return

        user = User.objects.get(id=user_id)
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        # Déterminer le payeur pour les cadeaux
        is_gift, payer = _parse_gift_metadata(metadata)
        invoice_owner = payer if is_gift and payer else user
        
        # Vérifier que c'est bien un paiement unique
        if plan_mode != 'one_time':
            plan_mode = _resolve_plan_mode(plan)
            if plan_mode != 'one_time':
                return

        niveau_obj = _get_niveau_from_id(niveau_id)

        # Éviter les doublons
        payment_intent = session.get('payment_intent') or ''
        if payment_intent:
            if AccessPass.objects.filter(stripe_payment_intent_id=payment_intent).exists():
                return
            if PaymentHistory.objects.filter(stripe_payment_intent_id=payment_intent).exists():
                return

        # Créer le pass d'accès (pour le bénéficiaire)
        days = _resolve_access_days(plan, metadata)
        start = timezone.now()
        ends = start + timedelta(days=days)

        AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=start,
            ends_at=ends,
            stripe_payment_intent_id=payment_intent or None
        )

        # Créer l'historique de paiement (pour le payeur/parent)
        payment_history, payment_created = _create_pass_payment_history(
            invoice_owner, user, plan, session, niveau_obj, payment_intent, start, ends, days, is_gift
        )

        if niveau_obj:
            _sync_user_niveau(user, niveau_obj)

        # Envoyer les emails
        if payment_created:
            _send_pass_emails(user, plan, niveau_obj, metadata, payment_history)

    except Exception as e:
        logger.error(f"Erreur dans handle_checkout_session_payment_completed: {e}")


def _create_pass_payment_history(invoice_owner, beneficiary, plan, session, niveau_obj, payment_intent, start, ends, days, is_gift=False):
    """Crée l'historique de paiement pour un pass.
    
    Pour les cadeaux, la facture est associée au payeur (invoice_owner) et non au bénéficiaire.
    """
    amount_total = session.get('amount_total')
    if not amount_total:
        return None, False

    currency = (session.get('currency') or 'eur').upper()
    level_label = _format_level_label_from_obj(niveau_obj)
    
    # Ajouter info bénéficiaire dans la description si c'est un cadeau
    beneficiary_info = ""
    if is_gift and beneficiary and invoice_owner != beneficiary:
        beneficiary_name = f"{beneficiary.first_name} {beneficiary.last_name}".strip() or beneficiary.email
        beneficiary_info = f" (pour {beneficiary_name})"

    return PaymentHistory.objects.get_or_create(
        user=invoice_owner,
        stripe_payment_intent_id=payment_intent or f"session_{session.get('id')}",
        defaults={
            'stripe_invoice_id': session.get('invoice'),
            'hosted_invoice_url': '',
            'invoice_pdf_url': '',
            'amount': amount_total / 100.0,
            'currency': currency,
            'status': 'succeeded',
            'description': _append_level_to_description(f"Pass {plan.name} ({days} jours){beneficiary_info}", level_label),
            'plan_name': plan.name,
            'plan_mode': 'one_time',
            'period_start': start,
            'period_end': ends,
            'niveau_pays': niveau_obj,
            'niveau_label': level_label,
        }
    )


def _send_pass_emails(user, plan, niveau_obj, metadata, payment_history):
    """Envoie les emails pour un achat de pass."""
    is_gift, payer = _parse_gift_metadata(metadata)

    try:
        if is_gift and payer:
            EmailService.send_gift_subscription_notification(
                recipient=user, gifter=payer, plan=plan, niveau=niveau_obj
            )
            EmailService.send_gift_purchase_confirmation(
                payer=payer, recipient=user, plan=plan, niveau=niveau_obj, is_pass=True
            )
        else:
            EmailService.send_subscription_confirmation(user, plan, niveau_obj)

        EmailService.send_new_subscription_notification_to_admin(
            user=user, plan=plan, niveau=niveau_obj, is_gift=is_gift, payer=payer
        )

        if payment_history:
            payment_history.email_sent = True
            payment_history.save(update_fields=['email_sent'])
            
    except Exception as exc:
        logger.error(f"Erreur envoi email pass: {exc}")


# =============================================================================
# Handler: invoice.payment_succeeded
# =============================================================================

def handle_payment_succeeded(invoice):
    """Gérer un paiement réussi."""
    try:
        invoice_id = invoice.get('id')
        
        # Récupérer les lignes si nécessaire
        if not invoice.get('lines') and invoice_id:
            invoice = stripe.Invoice.retrieve(invoice_id, expand=['lines'])

        # Vérifier que la facture est payée
        if not (invoice.get('paid') or invoice.get('status') == 'paid'):
            logger.info("handle_payment_succeeded: facture non payée (%s)", invoice_id)
            return

        subscription_id = invoice.get('subscription')
        if not subscription_id:
            return

        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription_data = _stripe_obj_to_dict(subscription)

        # Récupérer ou créer l'abonnement local
        user_subscription, previous_status = _get_or_create_subscription_from_invoice(
            subscription_id, subscription_data, invoice
        )
        if not user_subscription:
            return

        # Mettre à jour l'abonnement
        _update_subscription_status(user_subscription, subscription_data)

        # Récupérer les metadata pour déterminer le payeur
        metadata = subscription_data.get('metadata') or {}

        # Créer l'historique de paiement (associé au payeur si c'est un cadeau)
        payment_history, payment_created = _create_invoice_payment_history(
            user_subscription, invoice, invoice_id, metadata
        )

        # Déterminer si c'est la première charge
        is_first_charge = _is_first_charge(invoice, previous_status, subscription_data, payment_created)

        # Programmer l'envoi des emails
        if payment_history and not payment_history.email_sent:
            if is_first_charge:
                _schedule_subscription_emails(
                    payment_history_id=payment_history.id,
                    stripe_subscription_id=subscription_id,
                    metadata=metadata,
                )
            else:
                _schedule_invoice_email(
                    payment_history_id=payment_history.id,
                    stripe_subscription_id=subscription_id,
                    metadata=metadata,
                )

    except Exception as e:
        logger.error(f"Erreur dans handle_payment_succeeded: {e}")


def _get_or_create_subscription_from_invoice(subscription_id, subscription_data, invoice):
    """Récupère ou crée un UserSubscription depuis une facture."""
    try:
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)
        return user_subscription, user_subscription.status
    except UserSubscription.DoesNotExist:
        pass

    # Fallback: recréer depuis les metadata
    logger.warning("Souscription locale introuvable pour %s - fallback metadata", subscription_id)
    
    metadata = subscription_data.get('metadata') or {}
    invoice_meta = invoice.get('metadata') or {}
    user_id = metadata.get('user_id') or invoice_meta.get('user_id')
    plan_id = metadata.get('plan_id') or invoice_meta.get('plan_id')
    niveau_id = metadata.get('niveau_pays_id') or invoice_meta.get('niveau_pays_id')

    if not user_id or not plan_id:
        logger.error("Metadata manquante pour subscription=%s", subscription_id)
        return None, None

    user = User.objects.get(id=user_id)
    plan = SubscriptionPlan.objects.get(id=plan_id)
    niveau_obj = _get_niveau_from_id(niveau_id)

    defaults = _build_subscription_defaults(user, plan, subscription_data, niveau_obj)
    user_subscription, _ = UserSubscription.objects.get_or_create(
        stripe_subscription_id=subscription_id,
        defaults=defaults,
    )

    if niveau_obj:
        _sync_user_niveau(user, niveau_obj)

    return user_subscription, 'new'


def _update_subscription_status(user_subscription, subscription_data):
    """Met à jour le statut d'un abonnement depuis Stripe."""
    stripe_status = subscription_data.get('status')
    if stripe_status:
        user_subscription.status = stripe_status
    
    customer_id = subscription_data.get('customer')
    if customer_id:
        user_subscription.stripe_customer_id = customer_id

    for field, stripe_key in [
        ('current_period_start', 'current_period_start'),
        ('current_period_end', 'current_period_end'),
        ('trial_end', 'trial_end'),
    ]:
        value = _from_timestamp(subscription_data.get(stripe_key))
        if value:
            setattr(user_subscription, field, value)

    user_subscription.cancel_at_period_end = bool(
        subscription_data.get('cancel_at_period_end', user_subscription.cancel_at_period_end)
    )
    user_subscription.save()


def _create_invoice_payment_history(user_subscription, invoice, invoice_id, metadata=None):
    """Crée l'historique de paiement pour une facture.
    
    Pour les abonnements offerts (cadeaux), la facture est associée au payeur (parent)
    et non au bénéficiaire (enfant).
    """
    # Déterminer le propriétaire de la facture
    is_gift, payer = _parse_gift_metadata(metadata or {})
    invoice_owner = payer if is_gift and payer else user_subscription.user
    
    # Ajouter info bénéficiaire dans la description si c'est un cadeau
    beneficiary_info = ""
    if is_gift and payer:
        beneficiary = user_subscription.user
        beneficiary_name = f"{beneficiary.first_name} {beneficiary.last_name}".strip() or beneficiary.email
        beneficiary_info = f" (pour {beneficiary_name})"

    level_label = _format_level_label_from_obj(user_subscription.niveau_pays)
    period_start, period_end = _extract_invoice_period(invoice)
    hosted_invoice_url = (invoice.get('hosted_invoice_url') or '').strip()
    invoice_pdf_url = (invoice.get('invoice_pdf') or '').strip()

    payment_intent = invoice.get('payment_intent') or (f"invoice_{invoice_id}" if invoice_id else None)
    if not payment_intent:
        return None, False

    amount_paid = invoice.get('amount_paid') or invoice.get('total') or 0
    currency = (invoice.get('currency') or 'eur').upper()

    payment_history, created = PaymentHistory.objects.get_or_create(
        user=invoice_owner,
        stripe_invoice_id=invoice.get('id'),
        defaults={
            'stripe_payment_intent_id': payment_intent,
            'hosted_invoice_url': hosted_invoice_url,
            'invoice_pdf_url': invoice_pdf_url,
            'amount': amount_paid / 100,
            'currency': currency,
            'status': 'succeeded',
            'description': _append_level_to_description(
                f"Paiement pour {user_subscription.plan.name}{beneficiary_info}", level_label
            ),
            'plan_name': user_subscription.plan.name,
            'plan_mode': user_subscription.plan.plan_mode or 'subscription',
            'period_start': period_start,
            'period_end': period_end,
            'niveau_pays': user_subscription.niveau_pays,
            'niveau_label': level_label,
        }
    )

    # Mettre à jour les URLs si fournies après coup
    if payment_history:
        updates = []
        if hosted_invoice_url and payment_history.hosted_invoice_url != hosted_invoice_url:
            payment_history.hosted_invoice_url = hosted_invoice_url
            updates.append('hosted_invoice_url')
        if invoice_pdf_url and payment_history.invoice_pdf_url != invoice_pdf_url:
            payment_history.invoice_pdf_url = invoice_pdf_url
            updates.append('invoice_pdf_url')
        if updates:
            payment_history.save(update_fields=updates)

    return payment_history, created


def _is_first_charge(invoice, previous_status, subscription_data, payment_created):
    """Détermine si c'est la première charge d'un abonnement."""
    billing_reason = invoice.get('billing_reason')
    
    if billing_reason == 'subscription_create':
        return True
    
    # Conversion depuis trial
    stripe_status = subscription_data.get('status')
    if (billing_reason == 'subscription_cycle' and
        previous_status == 'trialing' and
        stripe_status and stripe_status != 'trialing'):
        return True
    
    # Fallback si billing_reason absent
    if billing_reason is None and payment_created:
        return True
    
    return False


# =============================================================================
# Handler: invoice.payment_failed
# =============================================================================

def handle_payment_failed(invoice):
    """Gérer un paiement échoué."""
    try:
        subscription_id = invoice.get('subscription')
        if not subscription_id:
            return
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)
        user_subscription.status = 'past_due'
        user_subscription.save(update_fields=['status'])
    except UserSubscription.DoesNotExist:
        logger.warning("handle_payment_failed: subscription introuvable (%s)", subscription_id)
    except Exception as e:
        logger.error(f"Erreur dans handle_payment_failed: {e}")


# =============================================================================
# Handler: customer.subscription.updated
# =============================================================================

def handle_subscription_updated(subscription):
    """Gérer la mise à jour d'un abonnement."""
    try:
        subscription = _stripe_obj_to_dict(subscription)
        stripe_subscription_id = subscription.get('id')
        if not stripe_subscription_id:
            return

        metadata = subscription.get('metadata') or {}
        
        with transaction.atomic():
            user_subscription = (
                UserSubscription.objects
                .select_for_update()
                .select_related('user', 'plan', 'niveau_pays', 'niveau_pays__pays')
                .get(stripe_subscription_id=stripe_subscription_id)
            )
            
            previous_cancel_at_period_end = bool(user_subscription.cancel_at_period_end)
            previous_status = user_subscription.status

            new_status = subscription.get('status', user_subscription.status)
            new_cancel_at_period_end = bool(subscription.get('cancel_at_period_end'))

            user_subscription.status = new_status
            user_subscription.current_period_start = _from_timestamp(subscription.get('current_period_start'))
            user_subscription.current_period_end = _from_timestamp(subscription.get('current_period_end'))
            user_subscription.cancel_at_period_end = new_cancel_at_period_end
            user_subscription.save()

            # Envoyer les emails de résiliation si nécessaire
            _schedule_cancellation_if_needed(
                user_subscription.id,
                stripe_subscription_id,
                metadata,
                previous_cancel_at_period_end,
                new_cancel_at_period_end,
                previous_status,
                new_status,
            )

    except UserSubscription.DoesNotExist:
        logger.warning("handle_subscription_updated: subscription introuvable (%s)", stripe_subscription_id)
    except Exception as e:
        logger.error(f"Erreur dans handle_subscription_updated: {e}")


def _schedule_cancellation_if_needed(us_id, sub_id, metadata, prev_cancel, new_cancel, prev_status, new_status):
    """Programme les emails de résiliation si nécessaire."""
    cancellation_scheduled = (not prev_cancel) and new_cancel
    canceled_immediately = (prev_status != 'canceled') and (new_status == 'canceled') and (not prev_cancel)

    if cancellation_scheduled:
        transaction.on_commit(lambda: _schedule_cancellation_emails(
            user_subscription_id=us_id,
            cancel_type='scheduled',
            stripe_subscription_id=sub_id,
            metadata=metadata,
        ))
    elif canceled_immediately:
        transaction.on_commit(lambda: _schedule_cancellation_emails(
            user_subscription_id=us_id,
            cancel_type='canceled',
            stripe_subscription_id=sub_id,
            metadata=metadata,
        ))


# =============================================================================
# Handler: customer.subscription.deleted
# =============================================================================

def handle_subscription_deleted(subscription):
    """Gérer la suppression d'un abonnement."""
    try:
        subscription = _stripe_obj_to_dict(subscription)
        stripe_subscription_id = subscription.get('id')
        if not stripe_subscription_id:
            return

        metadata = subscription.get('metadata') or {}
        
        with transaction.atomic():
            user_subscription = (
                UserSubscription.objects
                .select_for_update()
                .select_related('user', 'plan', 'niveau_pays', 'niveau_pays__pays')
                .get(stripe_subscription_id=stripe_subscription_id)
            )
            
            previous_cancel_at_period_end = bool(user_subscription.cancel_at_period_end)
            previous_status = user_subscription.status

            user_subscription.status = 'canceled'
            user_subscription.cancel_at_period_end = False
            user_subscription.current_period_end = (
                _from_timestamp(subscription.get('current_period_end')) or
                user_subscription.current_period_end
            )
            user_subscription.save()

            # Notifier seulement si pas déjà notifié via cancel_at_period_end
            if previous_status != 'canceled' and not previous_cancel_at_period_end:
                transaction.on_commit(lambda: _schedule_cancellation_emails(
                    user_subscription_id=user_subscription.id,
                    cancel_type='canceled',
                    stripe_subscription_id=stripe_subscription_id,
                    metadata=metadata,
                ))

    except UserSubscription.DoesNotExist:
        logger.warning("handle_subscription_deleted: subscription introuvable (%s)", stripe_subscription_id)
    except Exception as e:
        logger.error(f"Erreur dans handle_subscription_deleted: {e}")


__all__ = [
    'handle_invoice_created',
    'handle_checkout_session_completed',
    'handle_checkout_session_payment_completed',
    'handle_payment_succeeded',
    'handle_payment_failed',
    'handle_subscription_updated',
    'handle_subscription_deleted',
]
