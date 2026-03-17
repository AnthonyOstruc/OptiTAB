import json
from datetime import datetime, time as dt_time
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date
from decimal import Decimal
import logging

from .models import SubscriptionPlan, UserSubscription, PaymentHistory, AccessPass
from pays.models import Niveau
from django.db import DatabaseError
from django.db.models import Q
from stripe_config import (
    SUCCESS_URL,
    CANCEL_URL,
    FREE_TRIAL_DAYS,
    STRIPE_RUNTIME_MODE,
    get_stripe_webhook_secrets,
)
from core.services import EmailService
from .stripe_client import stripe, stripe_error
from .helpers import (
    _build_pass_description,
    _build_plan_payload,
    _extract_price_from_stripe_subscription,
    _format_level_label_from_obj,
    _from_timestamp,
    _is_stripe_subscription_active,
    _map_stripe_status,
    _resolve_payment_plan_mode,
    _resolve_payment_plan_name,
    _resolve_plan_mode,
)
from .stripe_services import (
    _clear_customer_temp_invoice_custom_fields,
    _build_gifted_subscriptions_from_stripe,
    _create_stripe_customer,
    _get_stripe_customer_id,
    _hydrate_payment_history_invoice,
    _list_stripe_subscriptions,
    _prime_customer_invoice_custom_fields,
    _refresh_subscription_from_snapshot,
    _refresh_subscription_from_stripe,
    _sync_level_subscriptions_from_stripe,
    _sync_payment_history_from_stripe,
)
from .handlers import (
    handle_charge_refunded,
    handle_checkout_session_completed,
    handle_checkout_session_payment_completed,
    handle_invoice_created,
    handle_payment_failed,
    handle_payment_succeeded,
    handle_refund_event,
    handle_subscription_deleted,
    handle_subscription_updated,
)
from .email_jobs import _schedule_cancellation_emails
from .subscription_status import build_subscription_status
from .pass_access import REFUNDED_STATUSES

logger = logging.getLogger(__name__)

User = get_user_model()



def _is_stripe_test_runtime():
    return str(STRIPE_RUNTIME_MODE).lower() == 'test'


def _construct_stripe_event(payload, sig_header):
    """Verify a webhook against the configured Stripe signing secrets."""
    webhook_secrets = get_stripe_webhook_secrets()
    if not webhook_secrets:
        logger.error("Stripe webhook: aucun secret de signature configuré")
        raise stripe_error.SignatureVerificationError(
            "No Stripe webhook signing secret configured.",
            sig_header or '',
        )

    last_signature_error = None
    for index, webhook_secret in enumerate(webhook_secrets):
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
            if index > 0:
                logger.info(
                    "Stripe webhook: signature validée avec un secret alternatif (slot=%s)",
                    index + 1,
                )
            return event
        except ValueError:
            raise
        except stripe_error.SignatureVerificationError as exc:
            last_signature_error = exc

    if last_signature_error is not None:
        raise last_signature_error

    raise stripe_error.SignatureVerificationError(
        "Unable to verify Stripe webhook signature.",
        sig_header or '',
    )


def _runtime_stripe_price_id(plan):
    if not plan:
        return None
    if _is_stripe_test_runtime():
        return (getattr(plan, 'stripe_price_id_test', None) or '').strip() or None
    return (getattr(plan, 'stripe_price_id', None) or '').strip() or None


def _find_plan_from_checkout_price_id(price_id):
    candidate = (price_id or '').strip()
    if not candidate:
        return None
    if _is_stripe_test_runtime():
        # Primary lookup in test field; fallback to live field for backward compatibility.
        return (
            SubscriptionPlan.objects.filter(stripe_price_id_test=candidate).first()
            or SubscriptionPlan.objects.filter(stripe_price_id=candidate).first()
        )
    return SubscriptionPlan.objects.filter(stripe_price_id=candidate).first()


def _plans_queryset_for_runtime():
    qs = SubscriptionPlan.objects.filter(is_active=True)
    if _is_stripe_test_runtime():
        # In local/dev test mode, only expose plans that are mapped to a test Price ID.
        return qs.exclude(stripe_price_id_test__isnull=True).exclude(stripe_price_id_test='')
    return qs


def _beneficiary_already_has_level_access(beneficiary_user, niveau_obj, *, now=None):
    """Retourne True si le bénéficiaire a déjà accès au niveau ciblé."""
    if not beneficiary_user or not niveau_obj:
        return False

    if getattr(beneficiary_user, 'has_complimentary_access', False):
        return True

    now = now or timezone.now()

    local_subscriptions = UserSubscription.objects.filter(
        user=beneficiary_user,
        niveau_pays=niveau_obj,
    ).only('status', 'cancel_at_period_end', 'current_period_end')
    if any(sub.is_active for sub in local_subscriptions):
        return True

    payment_intent_ids = list(
        PaymentHistory.objects.filter(
            plan_mode='one_time',
            niveau_pays=niveau_obj,
        )
        .exclude(status__in=REFUNDED_STATUSES)
        .exclude(stripe_payment_intent_id__isnull=True)
        .exclude(stripe_payment_intent_id='')
        .values_list('stripe_payment_intent_id', flat=True)
    )

    if payment_intent_ids and AccessPass.objects.filter(
        user=beneficiary_user,
        stripe_payment_intent_id__in=payment_intent_ids,
        ends_at__gt=now,
        is_revoked=False,
    ).exists():
        return True

    synced_subs = _sync_level_subscriptions_from_stripe(beneficiary_user, niveau_obj) or []
    return any(sub.is_active for sub in synced_subs)


class CreateCheckoutSessionView(APIView):
    """Créer une session de paiement Stripe"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Utiliser DRF pour parser le payload JSON
            price_id = request.data.get('price_id')
            niveau_payload = request.data.get('niveau_pays_id') or request.data.get('niveau_id')
            beneficiary_email = request.data.get('beneficiary_email')  # Email de l'élève (pour parents)
            
            logger.info("Checkout request user=%s niveau=%s price=%s beneficiary=%s", 
                       request.user.id, request.data.get('niveau_pays_id'), price_id, beneficiary_email)
            
            # Déterminer l'utilisateur bénéficiaire (l'élève ou soi-même)
            beneficiary_user = request.user
            payer_user = request.user
            
            if beneficiary_email:
                # Vérifier que le bénéficiaire est différent du payeur
                if beneficiary_email.strip().lower() == (request.user.email or '').lower():
                    return JsonResponse({
                        'error': "Vous ne pouvez pas utiliser votre propre email comme bénéficiaire."
                    }, status=400)
                
                # Chercher l'utilisateur bénéficiaire par email
                try:
                    beneficiary_user = User.objects.get(email__iexact=beneficiary_email.strip(), is_active=True)
                except User.DoesNotExist:
                    return JsonResponse({
                        'error': f"Aucun compte actif trouvé avec l'email {beneficiary_email}. L'élève doit d'abord créer son compte OptiTAB."
                    }, status=404)
                
                logger.info("User %s subscribing for beneficiary %s", payer_user.id, beneficiary_user.id)
            
            # Récupérer le plan depuis le price_id envoyé par le frontend.
            # En local/dev (Stripe test), on cible stripe_price_id_test quand il est configuré.
            plan = _find_plan_from_checkout_price_id(price_id)
            if not plan:
                return JsonResponse({'error': 'Plan non trouvé'}, status=404)
            checkout_price_id = _runtime_stripe_price_id(plan)
            if not checkout_price_id:
                mode_label = 'test' if _is_stripe_test_runtime() else 'live'
                return JsonResponse(
                    {'error': f"Plan non configuré pour Stripe {mode_label}. Configurez le price_id dans l'admin."},
                    status=400,
                )
            
            # Déterminer le niveau d'accès (obligatoire pour éviter l'accès global)
            niveau_obj = None
            if niveau_payload:
                try:
                    niveau_obj = Niveau.objects.get(id=niveau_payload, est_actif=True)
                except Niveau.DoesNotExist:
                    return JsonResponse({'error': 'Niveau sélectionné invalide'}, status=400)
            else:
                # Utiliser le niveau du bénéficiaire s'il existe
                niveau_obj = getattr(beneficiary_user, 'niveau_pays', None)

            if not niveau_obj:
                return JsonResponse({
                    'error': "Sélectionnez votre niveau scolaire pour finaliser l'abonnement."
                }, status=400)

            # Créer la session de checkout (abonnement récurrent ou pass unique)
            plan_mode = _resolve_plan_mode(plan)
            is_subscription = (plan_mode == 'subscription')

            # Cas parent -> enfant : éviter le doublon si le niveau est déjà débloqué.
            if beneficiary_email and _beneficiary_already_has_level_access(
                beneficiary_user,
                niveau_obj,
                now=timezone.now(),
            ):
                return JsonResponse({
                    'error': f"L'élève {beneficiary_user.email} a déjà ce niveau débloqué (abonnement ou pass actif)."
                }, status=400)

            # Pour les passes one-time en achat direct, éviter les doubles achats
            # si le niveau est déjà débloqué (abonnement/pass actif).
            if (not beneficiary_email) and (plan_mode == 'one_time') and _beneficiary_already_has_level_access(
                beneficiary_user,
                niveau_obj,
                now=timezone.now(),
            ):
                return JsonResponse({
                    'error': "Vous avez déjà ce niveau débloqué (abonnement ou pass actif)."
                }, status=400)

            # Créer ou récupérer le client Stripe (basé sur le payeur, pas le bénéficiaire)
            existing_customer_id = _get_stripe_customer_id(payer_user)
            if existing_customer_id:
                customer_id = existing_customer_id
                # Mettre à jour l'email du customer Stripe si différent
                try:
                    stripe.Customer.modify(customer_id, email=payer_user.email)
                except stripe_error.StripeError as e:
                    logger.warning(f"Could not update Stripe customer email: {e}")
            else:
                customer_id = _create_stripe_customer(payer_user)

            # Vérifier si le BÉNÉFICIAIRE a déjà un abonnement pour ce niveau
            if plan_mode == 'subscription':
                synced_subs = _sync_level_subscriptions_from_stripe(beneficiary_user, niveau_obj)
                if not synced_subs:
                    synced_subs = list(
                        UserSubscription.objects.filter(user=beneficiary_user, niveau_pays=niveau_obj)
                    )
                has_level_subscription = any(sub.is_active for sub in synced_subs)
                if not has_level_subscription:
                    try:
                        stripe_subscriptions = _list_stripe_subscriptions(payer_user)
                    except Exception:
                        stripe_subscriptions = []
                    beneficiary_id = str(beneficiary_user.id)
                    niveau_id = str(niveau_obj.id)
                    is_gift_checkout = bool(beneficiary_email)
                    for stripe_sub in stripe_subscriptions:
                        metadata = stripe_sub.get('metadata') or {}
                        meta_user_id = metadata.get('user_id')
                        if is_gift_checkout:
                            if not meta_user_id or str(meta_user_id) != beneficiary_id:
                                continue
                        elif meta_user_id and str(meta_user_id) != beneficiary_id:
                            continue
                        meta_niveau_id = metadata.get('niveau_pays_id')
                        # Vérifier uniquement si le niveau correspond - un abonnement
                        # pour un autre niveau avec le même plan n'est PAS un doublon
                        niveau_match = (meta_niveau_id and str(meta_niveau_id) == niveau_id)
                        if not niveau_match:
                            continue
                        if _is_stripe_subscription_active(stripe_sub):
                            has_level_subscription = True
                            break
                if has_level_subscription:
                    if beneficiary_email:
                        return JsonResponse({
                            'error': f"L'élève {beneficiary_user.email} a déjà un abonnement actif pour ce niveau."
                        }, status=400)
                    return JsonResponse({
                        'error': "Vous avez déjà un abonnement actif pour ce niveau."
                    }, status=400)

            # Metadata avec info sur le bénéficiaire
            metadata = {
                'user_id': str(beneficiary_user.id),  # L'abonnement est pour le bénéficiaire
                'payer_user_id': str(payer_user.id),  # Info sur qui a payé
                'plan_id': plan.id,
                'plan_mode': plan_mode,
                'niveau_pays_id': str(niveau_obj.id),
                'pays_id': str(niveau_obj.pays_id),
                'niveau_label': _format_level_label_from_obj(niveau_obj),
                'access_days': str(plan.access_days or ''),
            }
            
            # Ajouter l'info de souscription parent → enfant si applicable
            if beneficiary_email:
                beneficiary_full_name = f"{beneficiary_user.first_name} {beneficiary_user.last_name}".strip()
                metadata['is_gift'] = 'true'
                metadata['beneficiary_email'] = beneficiary_user.email
                metadata['beneficiary_name'] = beneficiary_full_name or beneficiary_user.email
            else:
                # S'assurer que le champ "Bénéficiaire" n'est PAS hérité d'un ancien achat cadeau
                # Nettoyer les custom_fields temporaires du Customer
                _clear_customer_temp_invoice_custom_fields(customer_id, names=['Bénéficiaire'])

            # Important: certains comptes Stripe finalisent immédiatement la 1ère facture d'une souscription.
            # Dans ce cas, invoice.created arrive trop tard pour modifier la facture. On prépare donc des
            # custom_fields au niveau Customer afin qu'ils soient hérités à la création.
            if is_subscription:
                _prime_customer_invoice_custom_fields(customer_id, metadata)

            create_kwargs = dict(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': checkout_price_id,
                    'quantity': 1,
                }],
                mode='subscription' if is_subscription else 'payment',
                success_url=SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=CANCEL_URL,
                metadata=metadata,
                # Personnalisation UI du checkout
                custom_text={
                    'submit': {
                        'message': 'Accès instantané après paiement. Facture disponible par email.'
                    }
                },
                locale='fr',  # Force la langue française
                allow_promotion_codes=True,  # Permet les codes promo
            )

            if is_subscription:
                subscription_data = {
                    'metadata': metadata
                }
                if FREE_TRIAL_DAYS > 0:
                    subscription_data['trial_period_days'] = FREE_TRIAL_DAYS
                create_kwargs['subscription_data'] = subscription_data
            else:
                # Pour les paiements uniques (passes), activer la création automatique de facture
                create_kwargs['invoice_creation'] = {
                    'enabled': True,
                    'invoice_data': {
                        'metadata': metadata,
                        'description': _build_pass_description(
                            plan.name,
                            level_label=_format_level_label_from_obj(niveau_obj),
                        ),
                    }
                }

            try:
                checkout_session = stripe.checkout.Session.create(**create_kwargs)
            except stripe_error.InvalidRequestError as exc:
                exc_message = str(exc).lower()
                if existing_customer_id and 'no such customer' in exc_message:
                    logger.info('Customer %s invalid, recreating for user %s', existing_customer_id, request.user.id)
                    new_customer_id = _create_stripe_customer(request.user)
                    UserSubscription.objects.filter(user=request.user, stripe_customer_id=existing_customer_id).update(
                        stripe_customer_id=new_customer_id
                    )
                    existing_customer_id = new_customer_id
                    create_kwargs['customer'] = new_customer_id
                    if is_subscription:
                        _prime_customer_invoice_custom_fields(new_customer_id, metadata)
                    checkout_session = stripe.checkout.Session.create(**create_kwargs)
                else:
                    raise
            
            return JsonResponse({'checkout_url': checkout_session.url})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# build_subscription_status a été déplacé vers subscription_status.py


class SubscriptionStatusView(APIView):
    """Récupérer le statut d'abonnement de l'utilisateur"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse(build_subscription_status(request.user))


class InvoiceListView(APIView):
    """Liste des factures Stripe de l'utilisateur"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_param = (request.GET.get('all', 'false').lower() == 'true')
        try:
            page = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            page = 1
        page = max(1, page)
        try:
            requested_limit = int(request.GET.get('limit', 50))
        except (TypeError, ValueError):
            requested_limit = 50
        requested_limit = max(1, min(requested_limit, 500))
        try:
            qs = PaymentHistory.objects.filter(user=request.user).order_by('-created_at')
            total_count = qs.count()
        except DatabaseError as exc:
            logger.error(f"InvoiceList DB error: {exc}")
            return JsonResponse({
                'detail': 'Factures indisponibles. Assurez-vous d\'avoir appliqué les dernières migrations backend.'
            }, status=503)
        sync_target = 200 if all_param else max(200, requested_limit * page)
        should_sync = all_param or (total_count < (requested_limit * page))

        # Synchroniser les factures Stripe au cas où le webhook n'aurait pas été reçu
        if should_sync:
            try:
                _sync_payment_history_from_stripe(request.user, limit=sync_target)
                qs = PaymentHistory.objects.filter(user=request.user).order_by('-created_at')
                total_count = qs.count()
            except Exception as sync_exc:
                logger.warning(f"Unable to sync invoices for user {request.user.id}: {sync_exc}")

        invoices = []
        if not all_param:
            offset = (page - 1) * requested_limit
            qs = qs[offset:offset + requested_limit]
        payments = list(qs)
        for payment in payments:
            pdf_url, hosted_url = _hydrate_payment_history_invoice(payment)
            plan_mode = _resolve_payment_plan_mode(payment)
            plan_name = _resolve_payment_plan_name(payment, plan_mode)
            invoices.append({
                'id': payment.id,
                'amount': float(payment.amount),
                'currency': payment.currency,
                'status': payment.status,
                'description': payment.description,
                'created_at': payment.created_at.isoformat(),
                'stripe_invoice_id': payment.stripe_invoice_id,
                'invoice_pdf_url': pdf_url,
                'hosted_invoice_url': hosted_url,
                'niveau_label': payment.niveau_label or _format_level_label_from_obj(payment.niveau_pays),
                'plan_name': plan_name,
                'plan_mode': plan_mode,
                'period_start': payment.period_start.isoformat() if payment.period_start else None,
                'period_end': payment.period_end.isoformat() if payment.period_end else None,
                'niveau_id': payment.niveau_pays_id,
            })
        payload = {'invoices': invoices}
        if not all_param:
            payload.update({
                'page': page,
                'page_size': requested_limit,
                'total': total_count
            })
        return JsonResponse(payload)


class InvoiceEmailView(APIView):
    """Envoi d'une facture par email"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            payment = PaymentHistory.objects.get(pk=pk, user=request.user)
        except PaymentHistory.DoesNotExist:
            return JsonResponse({'detail': 'Facture introuvable'}, status=404)
        except DatabaseError as exc:
            logger.error(f"InvoiceEmail DB error: {exc}")
            return JsonResponse({
                'detail': 'Factures indisponibles. Vérifiez les migrations backend.'
            }, status=503)

        pdf_url, hosted_url = _hydrate_payment_history_invoice(payment)
        invoice_link = pdf_url or hosted_url
        if not invoice_link:
            return JsonResponse({'detail': 'Cette facture n’est pas encore disponible.'}, status=400)

        try:
            EmailService.send_invoice_receipt(request.user, payment, invoice_link)
        except Exception as exc:
            logger.error(f"Erreur envoi facture {payment.id} à {request.user.email}: {exc}")
            return JsonResponse({'detail': 'Impossible d’envoyer la facture.'}, status=500)

        return JsonResponse({'sent': True})


class CheckoutSessionStatusView(APIView):
    """Valider manuellement une session Stripe (fallback si webhook indisponible)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session_id = request.query_params.get('session_id') or request.GET.get('session_id')
        if not session_id:
            return JsonResponse({'detail': 'session_id parameter is required'}, status=400)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe_error.InvalidRequestError:
            return JsonResponse({'detail': 'Session Stripe introuvable'}, status=404)
        except stripe_error.StripeError as exc:
            logger.error(f"Erreur Stripe lors de la récupération de la session {session_id}: {exc}")
            return JsonResponse({'detail': 'Impossible de récupérer la session Stripe'}, status=400)

        metadata = session.get('metadata') or {}
        session_user_id = metadata.get('user_id')
        payer_user_id = metadata.get('payer_user_id')  # Pour les achats parent → enfant
        is_gift = metadata.get('is_gift') == 'true'
        is_beneficiary = False
        is_payer = False
        
        # Vérifier que la session appartient à l'utilisateur (soit comme bénéficiaire, soit comme payeur)
        if session_user_id or payer_user_id:
            current_user_id = str(request.user.id)
            is_beneficiary = str(session_user_id) == current_user_id if session_user_id else False
            is_payer = str(payer_user_id) == current_user_id if payer_user_id else False
            
            if not is_beneficiary and not is_payer:
                return JsonResponse({'detail': 'Cette session ne correspond pas à votre compte'}, status=403)
        else:
            customer_email = (session.get('customer_details') or {}).get('email')
            user_email = (request.user.email or '').lower()
            if not customer_email:
                return JsonResponse({'detail': 'Cette session ne correspond pas à votre compte'}, status=403)
            if customer_email.lower() != (user_email or ''):
                return JsonResponse({'detail': 'Cette session ne correspond pas à votre compte'}, status=403)

        try:
            if session.get('subscription'):
                handle_checkout_session_completed(session)
            else:
                handle_checkout_session_payment_completed(session)
        except Exception as exc:
            logger.error(f"Erreur lors de la finalisation manuelle de la session Stripe {session_id}: {exc}")
            return JsonResponse({'detail': 'Impossible de finaliser cette session Stripe'}, status=500)

        request.user.refresh_from_db()
        status_payload = build_subscription_status(request.user)
        beneficiary_label = ''
        beneficiary_email = metadata.get('beneficiary_email')
        if beneficiary_email:
            beneficiary_label = beneficiary_email
        elif session_user_id:
            try:
                beneficiary_user = User.objects.filter(id=session_user_id).first()
                if beneficiary_user:
                    beneficiary_label = beneficiary_user.full_name or beneficiary_user.email or ''
            except Exception:
                beneficiary_label = ''

        payment_status = str(session.get('payment_status') or '').lower()
        currency = str(session.get('currency') or 'EUR').upper()
        amount_total_minor = session.get('amount_total')
        try:
            amount_total_minor = int(amount_total_minor) if amount_total_minor is not None else None
        except (TypeError, ValueError):
            amount_total_minor = None
        amount_total = (amount_total_minor / 100.0) if amount_total_minor is not None else None
        is_paid = bool(payment_status == 'paid' and amount_total_minor and amount_total_minor > 0)
        transaction_id = str(session.get('payment_intent') or session.get('id') or '')

        return JsonResponse({
            'status': status_payload,
            'has_access': status_payload.get('has_access', False),
            'session': {
                'is_gift': is_gift,
                'is_payer': is_payer,
                'is_beneficiary': is_beneficiary,
                'beneficiary_label': beneficiary_label
            },
            'payment': {
                'is_paid': is_paid,
                'status': payment_status,
                'value': amount_total,
                'value_minor': amount_total_minor,
                'currency': currency,
                'transaction_id': transaction_id,
            }
        })


def _normalize_metadata_user_id(value):
    if value in (None, ''):
        return None
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return str(value)


def _stripe_subscription_customer_email(stripe_sub):
    customer = stripe_sub.get('customer')
    if isinstance(customer, dict):
        return customer.get('email')
    if not customer:
        return None
    try:
        stripe_customer = stripe.Customer.retrieve(customer)
        if isinstance(stripe_customer, dict):
            return stripe_customer.get('email')
        return getattr(stripe_customer, 'email', None)
    except stripe_error.StripeError:
        return None


def _can_user_manage_subscription_from_stripe(user, stripe_sub):
    metadata = stripe_sub.get('metadata') or {}
    current_user_id = str(user.id)
    user_id = _normalize_metadata_user_id(metadata.get('user_id'))
    payer_id = _normalize_metadata_user_id(metadata.get('payer_user_id'))
    is_gift = str(metadata.get('is_gift') or '').lower() == 'true'
    has_beneficiary = bool(
        (metadata.get('beneficiary_email') or '').strip()
        or (metadata.get('beneficiary_name') or '').strip()
    )

    if is_gift or has_beneficiary:
        if payer_id:
            return current_user_id == payer_id
        customer_email = (_stripe_subscription_customer_email(stripe_sub) or '').lower()
        return bool(customer_email and customer_email == (user.email or '').lower())

    allowed_ids = {user_id, payer_id}
    allowed_ids.discard(None)
    if allowed_ids:
        return current_user_id in allowed_ids

    customer_email = (_stripe_subscription_customer_email(stripe_sub) or '').lower()
    return bool(customer_email and customer_email == (user.email or '').lower())


def _retrieve_stripe_subscription_for_management(stripe_subscription_id):
    try:
        stripe_sub = stripe.Subscription.retrieve(stripe_subscription_id, expand=['customer'])
        return stripe_sub, None
    except stripe_error.InvalidRequestError:
        return None, JsonResponse(
            {'error': 'Abonnement introuvable', 'message': 'Aucun abonnement correspondant trouvé.'},
            status=404
        )
    except stripe_error.StripeError as exc:
        logger.error(f"Stripe retrieve error {stripe_subscription_id}: {exc}")
        return None, JsonResponse(
            {'error': 'Stripe indisponible', 'message': 'Impossible de récupérer l\'abonnement Stripe.'},
            status=400
        )

class CancelSubscriptionView(APIView):
    """Annuler l'abonnement"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription_id = request.data.get('subscription_id')
        stripe_subscription_id = request.data.get('stripe_subscription_id')
        subscription = None

        stripe_sub_for_access = None

        if subscription_id:
            try:
                subscription = UserSubscription.objects.get(id=subscription_id, user=request.user)
            except (UserSubscription.DoesNotExist, ValueError):
                subscription = UserSubscription.objects.filter(stripe_subscription_id=subscription_id, user=request.user).first()

        if not subscription and stripe_subscription_id:
            subscription = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id, user=request.user).first()

        if not subscription and stripe_subscription_id:
            subscription = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()

        if subscription and subscription.user_id != request.user.id:
            if not subscription.stripe_subscription_id:
                return JsonResponse({'detail': 'Forbidden'}, status=403)
            stripe_sub_for_access, error_response = _retrieve_stripe_subscription_for_management(
                subscription.stripe_subscription_id
            )
            if error_response:
                return error_response
            if not _can_user_manage_subscription_from_stripe(request.user, stripe_sub_for_access):
                return JsonResponse({'detail': 'Forbidden'}, status=403)

        if subscription:
            was_scheduled = bool(subscription.cancel_at_period_end)
            was_canceled = (subscription.status == 'canceled')
            
            # Si déjà résilié ou programmé, ne pas renvoyer d'email
            if was_scheduled or was_canceled:
                if subscription.cancel_at_period_end:
                    message = 'Annulation déjà programmée à la fin de la période en cours.'
                else:
                    message = 'Abonnement déjà résilié.'
                return JsonResponse({'success': True, 'message': message})
            
            # Récupérer les metadata depuis Stripe pour savoir si c'est un cadeau
            cancellation_metadata = None
            if subscription.stripe_subscription_id:
                try:
                    stripe_sub = stripe_sub_for_access or stripe.Subscription.retrieve(subscription.stripe_subscription_id)
                    cancellation_metadata = stripe_sub.get('metadata') or {}
                except stripe_error.StripeError:
                    cancellation_metadata = {}
            
            if subscription.cancel_subscription():
                # Envoyer un email de confirmation de désabonnement (utilisateur + admin)
                if bool(subscription.cancel_at_period_end):
                    _schedule_cancellation_emails(
                        user_subscription_id=subscription.id,
                        cancel_type='scheduled',
                        stripe_subscription_id=subscription.stripe_subscription_id,
                        metadata=cancellation_metadata,
                    )
                elif subscription.status == 'canceled':
                    _schedule_cancellation_emails(
                        user_subscription_id=subscription.id,
                        cancel_type='canceled',
                        stripe_subscription_id=subscription.stripe_subscription_id,
                        metadata=cancellation_metadata,
                    )
                if subscription.cancel_at_period_end:
                    message = 'Annulation programmée à la fin de la période en cours.'
                else:
                    message = 'Abonnement résilié.'
                return JsonResponse({'success': True, 'message': message})
            return JsonResponse({'error': 'Erreur lors de l\'annulation', 'message': 'Impossible de programmer l\'annulation.'}, status=400)

        # Fallback sécurisé: annulation Stripe si l'abonnement n'est pas en base locale
        if stripe_subscription_id:
            stripe_sub, error_response = _retrieve_stripe_subscription_for_management(stripe_subscription_id)
            if error_response:
                return error_response
            if not _can_user_manage_subscription_from_stripe(request.user, stripe_sub):
                return JsonResponse({'detail': 'Forbidden'}, status=403)

            try:
                stripe.Subscription.modify(
                    stripe_subscription_id,
                    cancel_at_period_end=True
                )
            except stripe_error.StripeError as exc:
                logger.error(f"Stripe cancel error {stripe_subscription_id}: {exc}")
                return JsonResponse({'error': 'Stripe a refusé l\'annulation', 'message': 'Stripe a refusé l\'annulation.'}, status=400)

            return JsonResponse({'success': True, 'message': 'Annulation programmée à la fin de la période en cours.'})

        return JsonResponse({'error': 'Abonnement introuvable', 'message': 'Aucun abonnement correspondant trouvé.'}, status=404)


class ReactivateSubscriptionView(APIView):
    """Réactiver un abonnement programmé pour annulation (cancel_at_period_end=True)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription_id = request.data.get('subscription_id')
        stripe_subscription_id = request.data.get('stripe_subscription_id')
        subscription = None

        stripe_sub_for_access = None

        if subscription_id:
            try:
                subscription = UserSubscription.objects.get(id=subscription_id, user=request.user)
            except (UserSubscription.DoesNotExist, ValueError):
                subscription = UserSubscription.objects.filter(stripe_subscription_id=subscription_id, user=request.user).first()

        if not subscription and stripe_subscription_id:
            subscription = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id, user=request.user).first()

        if not subscription and stripe_subscription_id:
            subscription = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()

        if subscription and subscription.user_id != request.user.id:
            if not subscription.stripe_subscription_id:
                return JsonResponse({'detail': 'Forbidden'}, status=403)
            stripe_sub_for_access, error_response = _retrieve_stripe_subscription_for_management(
                subscription.stripe_subscription_id
            )
            if error_response:
                return error_response
            if not _can_user_manage_subscription_from_stripe(request.user, stripe_sub_for_access):
                return JsonResponse({'detail': 'Forbidden'}, status=403)

        if subscription:
            if not subscription.cancel_at_period_end:
                return JsonResponse({'success': True, 'message': 'Abonnement déjà actif.'})
            
            if subscription.status == 'canceled':
                return JsonResponse({'error': 'Abonnement déjà résilié', 'message': 'Cet abonnement est déjà résilié. Veuillez souscrire à un nouveau plan.'}, status=400)
            
            if not subscription.stripe_subscription_id:
                # Abonnement sans Stripe, réactiver localement
                subscription.cancel_at_period_end = False
                subscription.save(update_fields=['cancel_at_period_end', 'updated_at'])
                # Envoyer notification admin
                EmailService.send_reactivation_notification_to_admin(request.user, subscription)
                return JsonResponse({'success': True, 'message': 'Abonnement réactivé avec succès.'})

            try:
                stripe.Subscription.modify(
                    subscription.stripe_subscription_id,
                    cancel_at_period_end=False
                )
                updated = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
                if hasattr(updated, 'to_dict'):
                    updated = updated.to_dict()
                subscription.status = updated.get('status', subscription.status)
                subscription.cancel_at_period_end = bool(updated.get('cancel_at_period_end', False))
                subscription.save(update_fields=['status', 'cancel_at_period_end', 'updated_at'])
                # Envoyer notification admin
                EmailService.send_reactivation_notification_to_admin(request.user, subscription)
                return JsonResponse({'success': True, 'message': 'Abonnement réactivé avec succès ! Votre abonnement continuera normalement.'})
            except stripe_error.InvalidRequestError as exc:
                logger.warning(f"Stripe reactivate error {subscription.stripe_subscription_id}: {exc}")
                return JsonResponse({'error': 'Impossible de réactiver', 'message': 'Cet abonnement ne peut pas être réactivé.'}, status=400)
            except stripe_error.StripeError as exc:
                logger.error(f"Stripe reactivate error {subscription.stripe_subscription_id}: {exc}")
                return JsonResponse({'error': 'Stripe indisponible', 'message': 'Impossible de contacter Stripe pour le moment.'}, status=400)

        # Fallback: réactivation via stripe_subscription_id directement
        if stripe_subscription_id:
            stripe_sub, error_response = _retrieve_stripe_subscription_for_management(stripe_subscription_id)
            if error_response:
                return error_response
            if not _can_user_manage_subscription_from_stripe(request.user, stripe_sub):
                return JsonResponse({'detail': 'Forbidden'}, status=403)

            try:
                stripe.Subscription.modify(
                    stripe_subscription_id,
                    cancel_at_period_end=False
                )
                # Chercher l'abonnement local pour la notification
                local_sub = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()
                EmailService.send_reactivation_notification_to_admin(request.user, local_sub)
                return JsonResponse({'success': True, 'message': 'Abonnement réactivé avec succès !'})
            except stripe_error.StripeError as exc:
                logger.error(f"Stripe reactivate error {stripe_subscription_id}: {exc}")
                return JsonResponse({'error': 'Stripe a refusé la réactivation', 'message': 'Stripe a refusé la réactivation.'}, status=400)

        return JsonResponse({'error': 'Abonnement introuvable', 'message': 'Aucun abonnement correspondant trouvé.'}, status=404)


class PlansListView(APIView):
    """Liste des plans disponibles"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            plans = _plans_queryset_for_runtime().order_by('price')
            return JsonResponse({'plans': [_plan_to_dict(plan) for plan in plans]})
        except DatabaseError as e:
            logger.error(f"PlansListView DB error: {e}")
            return JsonResponse({
                'error': 'Database not ready. Run migrations and create plans in admin.',
                'hint': 'python manage.py migrate, then add SubscriptionPlan entries',
            }, status=500)

def _is_admin(user):
    try:
        return bool(getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False))
    except Exception:
        return False

def _iso_or_none(value):
    if not value:
        return None
    try:
        return value.isoformat()
    except Exception:
        return None

def _parse_bool_param(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raw = str(value).strip().lower()
    if raw in {'1', 'true', 'yes', 'y', 'on'}:
        return True
    if raw in {'0', 'false', 'no', 'n', 'off'}:
        return False
    return None

def _parse_datetime_value(value):
    if value in (None, ''):
        return None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        try:
            dt = datetime.fromtimestamp(value)
        except Exception:
            return None
    else:
        try:
            dt = parse_datetime(str(value))
        except Exception:
            dt = None
        if not dt:
            try:
                parsed_date = parse_date(str(value))
            except Exception:
                parsed_date = None
            if parsed_date:
                dt = datetime.combine(parsed_date, dt_time.min)
    if not dt:
        return None
    try:
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
    except Exception:
        pass
    return dt

def _plan_to_dict(plan, include_admin=False):
    runtime_price_id = _runtime_stripe_price_id(plan)
    payload = {
        'id': plan.id,
        'name': plan.name,
        'plan_type': plan.plan_type,
        'mode': _resolve_plan_mode(plan),
        'billing_period': plan.billing_period,
        'price': float(plan.price),
        # Expose the runtime-appropriate price ID to the public API.
        'stripe_price_id': runtime_price_id or plan.stripe_price_id,
        'features': plan.features,
        'access_days': getattr(plan, 'access_days', None),
    }
    if include_admin:
        payload.update({
            'is_active': plan.is_active,
            'created_at': plan.created_at.isoformat() if plan.created_at else None,
            'stripe_price_id_live': plan.stripe_price_id,
            'stripe_price_id_test': getattr(plan, 'stripe_price_id_test', None),
        })
    return payload

def _access_pass_to_dict(pass_obj, payment=None):
    plan = getattr(pass_obj, 'plan', None)
    plan_mode = _resolve_plan_mode(plan) if plan else 'one_time'
    payload = {
        'id': pass_obj.id,
        'user_id': pass_obj.user_id,
        'email': getattr(pass_obj.user, 'email', ''),
        'first_name': getattr(pass_obj.user, 'first_name', ''),
        'last_name': getattr(pass_obj.user, 'last_name', ''),
        'plan_id': getattr(pass_obj, 'plan_id', None),
        'plan_name': getattr(plan, 'name', None) if plan else None,
        'plan_mode': plan_mode,
        'access_days': getattr(plan, 'access_days', None) if plan else None,
        'starts_at': _iso_or_none(getattr(pass_obj, 'starts_at', None)),
        'ends_at': _iso_or_none(getattr(pass_obj, 'ends_at', None)),
        'created_at': _iso_or_none(getattr(pass_obj, 'created_at', None)),
        'stripe_payment_intent_id': getattr(pass_obj, 'stripe_payment_intent_id', None),
        'is_active': pass_obj.is_active,
        'is_revoked': getattr(pass_obj, 'is_revoked', False),
        'revoked_at': _iso_or_none(getattr(pass_obj, 'revoked_at', None)),
    }
    if payment is not None:
        try:
            payload['amount_paid'] = float(payment.amount)
        except Exception:
            payload['amount_paid'] = None
        payload['currency'] = getattr(payment, 'currency', None)
        payload['payment_status'] = getattr(payment, 'status', None)
        payload['payment_description'] = getattr(payment, 'description', None)
    return payload

class AdminPlansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        qs = SubscriptionPlan.objects.all().order_by('-is_active', 'price')
        return JsonResponse({'plans': [_plan_to_dict(p, include_admin=True) for p in qs]})

    def post(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        data = request.data if hasattr(request, 'data') else json.loads(request.body or '{}')
        try:
            name = data.get('name') or ''
            plan_type = data.get('plan_type') or 'basic'
            mode = (data.get('mode') or data.get('plan_mode') or 'subscription').lower()
            billing_period = data.get('billing_period') or 'monthly'
            price = data.get('price')
            stripe_price_id = data.get('stripe_price_id')
            stripe_price_id_test = (data.get('stripe_price_id_test') or None)
            access_days = data.get('access_days')
            features = data.get('features') or []
            is_active = bool(data.get('is_active', True))

            if not name or not stripe_price_id or price is None:
                return JsonResponse({'detail': 'name, price and stripe_price_id are required'}, status=400)

            plan = SubscriptionPlan.objects.create(
                name=name,
                plan_type=plan_type,
                billing_period=billing_period,
                price=price,
                stripe_price_id=stripe_price_id,
                stripe_price_id_test=stripe_price_id_test,
                features=features if isinstance(features, list) else [],
                is_active=is_active,
            )
            # set mode/access_days if fields exist
            if hasattr(plan, 'plan_mode'):
                plan.plan_mode = mode
            if hasattr(plan, 'mode'):
                setattr(plan, 'mode', mode)
            if hasattr(plan, 'access_days') and access_days is not None:
                plan.access_days = access_days
            plan.save()
            return JsonResponse({'plan': _plan_to_dict(plan, include_admin=True)}, status=201)
        except Exception as e:
            logger.error(f"AdminPlansView.post error: {e}")
            return JsonResponse({'detail': str(e)}, status=400)

class AdminPlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        try:
            plan = SubscriptionPlan.objects.get(pk=pk)
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({'detail': 'Not found'}, status=404)
        data = request.data if hasattr(request, 'data') else json.loads(request.body or '{}')
        try:
            for field in ['name', 'plan_type', 'billing_period', 'price', 'stripe_price_id', 'stripe_price_id_test', 'is_active']:
                if field in data:
                    value = data[field]
                    if field == 'stripe_price_id_test' and value in ('', None):
                        value = None
                    setattr(plan, field, value)
            # Handle mode / plan_mode
            if 'mode' in data or 'plan_mode' in data:
                mode = (data.get('mode') or data.get('plan_mode')).lower()
                if hasattr(plan, 'plan_mode'):
                    plan.plan_mode = mode
                if hasattr(plan, 'mode'):
                    setattr(plan, 'mode', mode)
            if 'access_days' in data and hasattr(plan, 'access_days'):
                plan.access_days = data.get('access_days')
            if 'features' in data and isinstance(data['features'], list):
                plan.features = data['features']
            plan.save()
            return JsonResponse({'plan': _plan_to_dict(plan, include_admin=True)})
        except Exception as e:
            logger.error(f"AdminPlanDetailView.patch error: {e}")
            return JsonResponse({'detail': str(e)}, status=400)

    def delete(self, request, pk):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        try:
            plan = SubscriptionPlan.objects.get(pk=pk)
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({'detail': 'Not found'}, status=404)
        plan.delete()
        return JsonResponse({'deleted': True})


class AdminSubscribersView(APIView):
    """Liste consolidée des abonnés (abonnements + passes) pour l'admin"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        try:
            q = (request.GET.get('q') or '').strip().lower()
            active_only = (request.GET.get('active', 'false').lower() == 'true')

            items = []
            covered_user_ids = set()

            # Abonnements récurrents
            subs_qs = UserSubscription.objects.select_related('user', 'plan')
            # Précharger le montant du dernier paiement pour chaque abonnement (si disponible)
            latest_payment_map = {}
            try:
                latest_payments = (
                    PaymentHistory.objects
                    .filter(stripe_payment_intent_id__isnull=False)
                    .order_by('user_id', '-created_at')
                )
                for payment in latest_payments:
                    if payment.user_id in latest_payment_map:
                        continue
                    latest_payment_map[payment.user_id] = {
                        'amount': float(payment.amount),
                        'currency': (payment.currency or 'EUR').upper(),
                    }
            except Exception as payment_err:
                logger.warning(f"AdminSubscribersView payment lookup failed: {payment_err}")
                latest_payment_map = {}
            for s in subs_qs:
                try:
                    if q:
                        if q not in (s.user.email or '').lower() and q not in (s.user.first_name or '').lower() and q not in (s.user.last_name or '').lower():
                            continue
                    plan = getattr(s, 'plan', None)
                    plan_name = getattr(plan, 'name', '—') if plan else '—'
                    plan_mode = _resolve_plan_mode(plan) if plan else 'subscription'
                    billing_period = getattr(plan, 'billing_period', None) if plan else None
                    rec = {
                        'type': 'subscription',
                        'subscription_id': s.id,
                        'stripe_subscription_id': s.stripe_subscription_id,
                        'user_id': s.user_id,
                        'email': getattr(s.user, 'email', ''),
                        'first_name': getattr(s.user, 'first_name', ''),
                        'last_name': getattr(s.user, 'last_name', ''),
                        'plan_id': getattr(s, 'plan_id', None),
                        'plan_name': plan_name,
                        'plan_mode': plan_mode,
                        'billing_period': billing_period,
                        'status': s.status,
                        'is_active': bool(getattr(s, 'is_active', False)),
                        'is_trial': bool(getattr(s, 'is_trial', False)),
                        'days_remaining_trial': int(getattr(s, 'days_remaining_trial', 0)),
                        'current_period_start': _iso_or_none(getattr(s, 'current_period_start', None)),
                        'current_period_end': _iso_or_none(getattr(s, 'current_period_end', None)),
                        'cancel_at_period_end': bool(getattr(s, 'cancel_at_period_end', False)),
                    }
                    payment_info = latest_payment_map.get(s.user_id)
                    if payment_info:
                        rec.update({
                            'amount_paid': payment_info['amount'],
                            'currency': payment_info['currency'],
                        })
                    elif plan and getattr(plan, 'price', None) is not None:
                        rec.update({
                            'amount_paid': float(plan.price),
                            'currency': 'EUR',
                        })
                    if active_only and not rec['is_active']:
                        continue
                    items.append(rec)
                    covered_user_ids.add(s.user_id)
                except Exception as row_err:
                    logger.error(f"AdminSubscribersView row(sub) error: {row_err}")
                    continue

            # Pass (achats one-time)
            now = timezone.now()
            try:
                pass_qs = AccessPass.objects.select_related('user', 'plan')
                for p in pass_qs:
                    try:
                        if q:
                            if q not in (p.user.email or '').lower() and q not in (p.user.first_name or '').lower() and q not in (p.user.last_name or '').lower():
                                continue
                        plan = getattr(p, 'plan', None)
                        plan_name = getattr(plan, 'name', '—') if plan else '—'
                        plan_mode = _resolve_plan_mode(plan) if plan else 'one_time'
                        access_days = getattr(plan, 'access_days', None) if plan else None
                        is_active = p.is_active  # Prend en compte is_revoked
                        if active_only and not is_active:
                            continue
                        pass_entry = {
                            'type': 'pass',
                            'user_id': p.user_id,
                            'email': getattr(p.user, 'email', ''),
                            'first_name': getattr(p.user, 'first_name', ''),
                            'last_name': getattr(p.user, 'last_name', ''),
                            'plan_id': getattr(p, 'plan_id', None),
                            'plan_name': plan_name,
                            'plan_mode': plan_mode,
                            'access_days': access_days,
                            'starts_at': _iso_or_none(getattr(p, 'starts_at', None)),
                            'ends_at': _iso_or_none(getattr(p, 'ends_at', None)),
                            'is_active': is_active,
                            'is_revoked': getattr(p, 'is_revoked', False),
                        }
                        if plan and getattr(plan, 'price', None) is not None:
                            pass_entry['amount_paid'] = float(plan.price)
                            pass_entry['currency'] = 'EUR'
                        items.append(pass_entry)
                        covered_user_ids.add(p.user_id)
                    except Exception as row_err:
                        logger.error(f"AdminSubscribersView row(pass) error: {row_err}")
                        continue
            except DatabaseError as access_pass_err:
                logger.warning(f"AdminSubscribersView pass query skipped (likely unmigrated): {access_pass_err}")
                # Pas de table (migrations non appliquées) -> ignorer silencieusement côté UI

            # Accès manuels accordés par un administrateur
            try:
                manual_qs = User.objects.filter(has_complimentary_access=True)
                for user in manual_qs:
                    try:
                        if user.id in covered_user_ids:
                            continue
                        if q:
                            if q not in (user.email or '').lower() and q not in (user.first_name or '').lower() and q not in (user.last_name or '').lower():
                                continue
                        manual_entry = {
                            'type': 'manual',
                            'user_id': user.id,
                            'email': getattr(user, 'email', ''),
                            'first_name': getattr(user, 'first_name', ''),
                            'last_name': getattr(user, 'last_name', ''),
                            'plan_id': None,
                            'plan_name': 'Accès manuel',
                            'plan_mode': 'manual',
                            'billing_period': None,
                            'status': 'manual',
                            'is_active': True,
                            'is_trial': False,
                            'days_remaining_trial': 0,
                            'current_period_start': _iso_or_none(getattr(user, 'date_joined', None)),
                            'current_period_end': None,
                            'amount_paid': None,
                            'currency': None,
                        }
                        if active_only and not manual_entry['is_active']:
                            continue
                        items.append(manual_entry)
                        covered_user_ids.add(user.id)
                    except Exception as manual_err:
                        logger.error(f"AdminSubscribersView row(manual) error: {manual_err}")
                        continue
            except Exception as manual_qs_err:
                logger.warning(f"AdminSubscribersView manual list failed: {manual_qs_err}")

            # Tri: éléments actifs en premier, puis par date de fin croissante
            def key_fn(x):
                end = x.get('current_period_end') or x.get('ends_at') or ''
                return (0 if x.get('is_active') else 1, end)
            items.sort(key=key_fn)

            return JsonResponse({'items': items, 'total': len(items)})
        except Exception as e:
            logger.error(f"AdminSubscribersView.get error: {e}")
            # Ne pas bloquer l'UI admin: retourner une liste vide avec le message d'erreur
            return JsonResponse({'items': [], 'total': 0, 'error': str(e)}, status=200)


class AdminPassesView(APIView):
    """Liste des passes (one-time) pour l'admin"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        q = (request.GET.get('q') or '').strip().lower()
        active_param = _parse_bool_param(request.GET.get('active'))
        revoked_param = _parse_bool_param(request.GET.get('revoked'))

        qs = AccessPass.objects.select_related('user', 'plan').order_by('-starts_at')

        if q:
            qs = qs.filter(
                Q(user__email__icontains=q)
                | Q(user__first_name__icontains=q)
                | Q(user__last_name__icontains=q)
                | Q(stripe_payment_intent_id__icontains=q)
            )

        if revoked_param is True:
            qs = qs.filter(is_revoked=True)
        elif revoked_param is False:
            qs = qs.filter(is_revoked=False)

        if active_param is True:
            qs = qs.filter(is_revoked=False, ends_at__gt=timezone.now())
        elif active_param is False:
            qs = qs.filter(Q(is_revoked=True) | Q(ends_at__lte=timezone.now()))

        pass_list = list(qs)
        payment_map = {}
        try:
            pi_ids = [p.stripe_payment_intent_id for p in pass_list if p.stripe_payment_intent_id]
            if pi_ids:
                for payment in PaymentHistory.objects.filter(stripe_payment_intent_id__in=pi_ids):
                    payment_map[payment.stripe_payment_intent_id] = payment
        except Exception as payment_err:
            logger.warning(f"AdminPassesView payment lookup failed: {payment_err}")

        payload = [_access_pass_to_dict(p, payment_map.get(p.stripe_payment_intent_id)) for p in pass_list]
        return JsonResponse({'passes': payload, 'total': len(payload)})


class AdminPassDetailView(APIView):
    """Mise Ã  jour rapide d'un pass (rÃ©vocation, dates)"""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        try:
            access_pass = AccessPass.objects.select_related('user', 'plan').get(pk=pk)
        except AccessPass.DoesNotExist:
            return JsonResponse({'detail': 'Not found'}, status=404)

        data = request.data if hasattr(request, 'data') else json.loads(request.body or '{}')
        updates = []

        if 'starts_at' in data:
            parsed = _parse_datetime_value(data.get('starts_at'))
            if not parsed:
                return JsonResponse({'detail': 'starts_at invalide'}, status=400)
            access_pass.starts_at = parsed
            updates.append('starts_at')

        if 'ends_at' in data:
            parsed = _parse_datetime_value(data.get('ends_at'))
            if not parsed:
                return JsonResponse({'detail': 'ends_at invalide'}, status=400)
            access_pass.ends_at = parsed
            updates.append('ends_at')

        if 'is_revoked' in data:
            is_revoked = _parse_bool_param(data.get('is_revoked'))
            if is_revoked is None:
                return JsonResponse({'detail': 'is_revoked invalide'}, status=400)
            access_pass.is_revoked = is_revoked
            access_pass.revoked_at = timezone.now() if is_revoked else None
            updates.extend(['is_revoked', 'revoked_at'])

        if 'starts_at' in data and 'ends_at' in data:
            if access_pass.ends_at and access_pass.starts_at and access_pass.ends_at < access_pass.starts_at:
                return JsonResponse({'detail': 'ends_at doit Ãªtre aprÃ¨s starts_at'}, status=400)

        if updates:
            access_pass.save(update_fields=list(dict.fromkeys(updates)))

        payment = None
        try:
            if access_pass.stripe_payment_intent_id:
                payment = PaymentHistory.objects.filter(
                    stripe_payment_intent_id=access_pass.stripe_payment_intent_id
                ).first()
        except Exception:
            payment = None

        return JsonResponse({'pass': _access_pass_to_dict(access_pass, payment)})


class AdminStripeSyncView(APIView):
    """Synchronise les abonnements Stripe → base locale (abonnements récurrents)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        try:
            synced, created, updated, skipped, created_plans = 0, 0, 0, 0, 0

            # Helper: ensure local plan exists from a Stripe price id
            def ensure_plan_from_price(price_id):
                nonlocal created_plans
                plan = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()
                if plan:
                    return plan
                try:
                    price = stripe.Price.retrieve(price_id, expand=['product'])
                except Exception as e:
                    logger.error(f"Cannot retrieve Stripe price {price_id}: {e}")
                    return None

                amount = price.get('unit_amount') or price.get('unit_amount_decimal') or 0
                try:
                    amount = Decimal(str(amount)) / Decimal('100')
                except Exception:
                    amount = Decimal('0')

                interval = (price.get('recurring') or {}).get('interval') or 'month'
                billing_period = 'monthly'
                if interval == 'year':
                    billing_period = 'yearly'
                elif interval == 'day':
                    billing_period = 'daily'
                elif interval == 'week':
                    billing_period = 'weekly'

                product_name = None
                try:
                    product = price.get('product')
                    if isinstance(product, dict):
                        product_name = product.get('name')
                except Exception:
                    product_name = None
                name = price.get('nickname') or product_name or f"Plan {price_id}"

                plan = SubscriptionPlan.objects.create(
                    name=name,
                    plan_type='basic',
                    billing_period=billing_period,
                    price=amount,
                    stripe_price_id=price_id,
                    features=[],
                    is_active=True,
                )
                # for compatibility with plan_mode/mode
                if hasattr(plan, 'plan_mode'):
                    plan.plan_mode = 'subscription'
                    plan.save()
                elif hasattr(plan, 'mode'):
                    setattr(plan, 'mode', 'subscription')
                    plan.save()
                created_plans += 1
                return plan

            # Fetch subscriptions from Stripe with expansions for easier mapping
            # Some Stripe accounts reject unknown 'status' filters; omit for full list
            try:
                subs = stripe.Subscription.list(limit=100, expand=['data.customer', 'data.items.data.price.product'])
            except Exception as list_err:
                logger.warning(f"Stripe list with expand failed, falling back: {list_err}")
                subs = stripe.Subscription.list(limit=100)
            for s in subs.auto_paging_iter():
                try:
                    meta = getattr(s, 'metadata', None) or {}
                    user_id = meta.get('user_id')
                    plan_id_meta = meta.get('plan_id')

                    # Fallback: customer metadata or email → local user
                    customer_email = None
                    if getattr(s, 'customer', None):
                        try:
                            cust = s.customer if isinstance(s.customer, dict) else stripe.Customer.retrieve(s.customer)
                            customer_email = (cust.get('email') if isinstance(cust, dict) else getattr(cust, 'email', None)) or None
                            user_id = user_id or ((cust.get('metadata') or {}).get('user_id') if isinstance(cust, dict) else (getattr(cust, 'metadata', {}) or {}).get('user_id'))
                        except Exception:
                            pass

                    user = None
                    if user_id:
                        try:
                            user = User.objects.get(pk=int(user_id))
                        except Exception:
                            user = None
                    if user is None and customer_email:
                        try:
                            user = User.objects.filter(email__iexact=customer_email).first()
                        except Exception:
                            user = None
                    if user is None:
                        skipped += 1
                        continue

                    # Determine local plan
                    plan = None
                    if plan_id_meta:
                        try:
                            plan = SubscriptionPlan.objects.filter(pk=int(plan_id_meta)).first()
                        except Exception:
                            plan = None
                    if plan is None:
                        try:
                            price_id = s['items']['data'][0]['price']['id']
                        except Exception:
                            price_id = None
                        if price_id:
                            plan = ensure_plan_from_price(price_id)
                    if plan is None:
                        skipped += 1
                        continue

                    stripe_sub_id = getattr(s, 'id', None)
                    if not stripe_sub_id:
                        skipped += 1
                        continue

                    niveau_obj = None
                    niveau_id = meta.get('niveau_pays_id')
                    if niveau_id:
                        try:
                            niveau_obj = Niveau.objects.get(id=int(niveau_id), est_actif=True)
                        except (Niveau.DoesNotExist, ValueError, TypeError):
                            niveau_obj = None

                    defaults = {
                        'user': user,
                        'plan': plan,
                        'stripe_customer_id': s.customer['id'] if isinstance(s.customer, dict) else s.customer,
                        'status': s.status,
                        'current_period_start': _from_timestamp(getattr(s, 'current_period_start', None)),
                        'current_period_end': _from_timestamp(getattr(s, 'current_period_end', None)),
                        'trial_end': _from_timestamp(getattr(s, 'trial_end', None)),
                        'cancel_at_period_end': bool(getattr(s, 'cancel_at_period_end', False)),
                        'niveau_pays': niveau_obj,
                    }

                    obj, was_created = UserSubscription.objects.update_or_create(
                        stripe_subscription_id=stripe_sub_id,
                        defaults=defaults,
                    )
                    synced += 1
                    if was_created:
                        created += 1
                    else:
                        updated += 1
                except Exception as inner:
                    logger.error(f"Sync item error: {inner}")
                    skipped += 1

            return JsonResponse({'synced': synced, 'created': created, 'updated': updated, 'skipped': skipped, 'created_plans': created_plans})
        except Exception as e:
            logger.error(f"AdminStripeSyncView.post error: {e}")
            return JsonResponse({'detail': 'Server error', 'error': str(e)}, status=500)


class AdminSubscriptionPlanChangeView(APIView):
    """Permet aux administrateurs de changer le plan d'un abonnement utilisateur."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        data = request.data if hasattr(request, 'data') else json.loads(request.body or '{}')
        subscription_id = data.get('subscription_id')
        stripe_subscription_id = data.get('stripe_subscription_id')
        plan_id = data.get('plan_id') or data.get('new_plan_id')

        if not plan_id:
            return JsonResponse({'detail': 'plan_id requis'}, status=400)

        subscription = None
        if subscription_id:
            try:
                subscription = UserSubscription.objects.select_related('plan').get(pk=subscription_id)
            except (UserSubscription.DoesNotExist, ValueError, TypeError):
                subscription = None

        if not subscription and stripe_subscription_id:
            subscription = (
                UserSubscription.objects
                .select_related('plan')
                .filter(stripe_subscription_id=stripe_subscription_id)
                .first()
            )

        if not subscription:
            return JsonResponse({'detail': 'Abonnement introuvable'}, status=404)

        try:
            target_plan = SubscriptionPlan.objects.get(pk=int(plan_id))
        except (SubscriptionPlan.DoesNotExist, ValueError, TypeError):
            return JsonResponse({'detail': 'Plan introuvable'}, status=404)

        target_mode = _resolve_plan_mode(target_plan)
        if target_mode != 'subscription':
            return JsonResponse({'detail': 'Le plan cible doit être un abonnement récurrent.'}, status=400)
        if not getattr(target_plan, 'is_active', True):
            return JsonResponse({'detail': 'Le plan cible est inactif.'}, status=400)

        current_mode = _resolve_plan_mode(getattr(subscription, 'plan', None))
        if current_mode != 'subscription':
            return JsonResponse({'detail': "Ce changement n'est autorisé que pour les abonnements récurrents."}, status=400)

        if subscription.plan_id == target_plan.id:
            return JsonResponse({
                'success': True,
                'message': 'Le plan est déjà appliqué.',
                'subscription': {
                    'id': subscription.id,
                    'plan_id': subscription.plan_id,
                    'plan_name': getattr(subscription.plan, 'name', ''),
                    'status': subscription.status,
                    'cancel_at_period_end': bool(subscription.cancel_at_period_end),
                    'current_period_end': _iso_or_none(subscription.current_period_end),
                }
            })

        updated_fields = ['plan', 'updated_at']

        # Si l'abonnement est relié à Stripe, on bascule également le Price ID côté Stripe
        # pour conserver la cohérence entre la facturation et la base locale.
        if subscription.stripe_subscription_id:
            stripe_price_id = _runtime_stripe_price_id(target_plan)
            if not stripe_price_id:
                mode_label = 'test' if _is_stripe_test_runtime() else 'live'
                return JsonResponse({
                    'detail': f"Le plan cible n'est pas configuré pour Stripe {mode_label}."
                }, status=400)

            try:
                stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
                if hasattr(stripe_sub, 'to_dict'):
                    stripe_sub = stripe_sub.to_dict()

                stripe_items = ((stripe_sub.get('items') or {}).get('data') or [])
                stripe_item_id = stripe_items[0].get('id') if stripe_items else None
                if not stripe_item_id:
                    return JsonResponse({
                        'detail': 'Impossible de modifier cet abonnement côté Stripe (item manquant).'
                    }, status=400)

                stripe_metadata = stripe_sub.get('metadata') or {}
                if not isinstance(stripe_metadata, dict):
                    stripe_metadata = {}
                stripe_metadata.update({
                    'plan_id': str(target_plan.id),
                    'plan_mode': target_mode,
                })

                updated_sub = stripe.Subscription.modify(
                    subscription.stripe_subscription_id,
                    items=[{
                        'id': stripe_item_id,
                        'price': stripe_price_id,
                    }],
                    proration_behavior='none',
                    metadata=stripe_metadata,
                )
                if hasattr(updated_sub, 'to_dict'):
                    updated_sub = updated_sub.to_dict()

                subscription.status = updated_sub.get('status', subscription.status)
                subscription.current_period_start = (
                    _from_timestamp(updated_sub.get('current_period_start'))
                    or subscription.current_period_start
                )
                subscription.current_period_end = (
                    _from_timestamp(updated_sub.get('current_period_end'))
                    or subscription.current_period_end
                )
                subscription.trial_end = (
                    _from_timestamp(updated_sub.get('trial_end'))
                    or subscription.trial_end
                )
                subscription.cancel_at_period_end = bool(
                    updated_sub.get('cancel_at_period_end', subscription.cancel_at_period_end)
                )
                updated_fields.extend([
                    'status',
                    'current_period_start',
                    'current_period_end',
                    'trial_end',
                    'cancel_at_period_end',
                ])
            except stripe_error.StripeError as exc:
                human = getattr(exc, 'user_message', None) or str(exc)
                return JsonResponse({
                    'detail': f"Stripe a refusé le changement de plan ({human})."
                }, status=400)
            except Exception as exc:
                logger.error(
                    "AdminSubscriptionPlanChange unexpected error for sub %s: %s",
                    subscription.id,
                    exc,
                )
                return JsonResponse({'detail': 'Erreur serveur pendant la mise à jour Stripe.'}, status=500)

        subscription.plan = target_plan
        subscription.save(update_fields=list(dict.fromkeys(updated_fields)))

        return JsonResponse({
            'success': True,
            'message': f"Plan mis à jour vers {target_plan.name}.",
            'subscription': {
                'id': subscription.id,
                'plan_id': target_plan.id,
                'plan_name': target_plan.name,
                'status': subscription.status,
                'cancel_at_period_end': bool(subscription.cancel_at_period_end),
                'current_period_end': _iso_or_none(subscription.current_period_end),
            }
        })


class AdminSubscriptionCancelView(APIView):
    """Permet aux administrateurs de résilier un abonnement utilisateur."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        data = request.data if hasattr(request, 'data') else json.loads(request.body or '{}')
        subscription_id = data.get('subscription_id')
        stripe_subscription_id = data.get('stripe_subscription_id')
        immediate = bool(data.get('immediate', False))

        subscription = None
        if subscription_id:
            try:
                subscription = UserSubscription.objects.get(pk=subscription_id)
            except (UserSubscription.DoesNotExist, ValueError):
                subscription = None

        if not subscription and stripe_subscription_id:
            subscription = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id).first()

        if not subscription:
            return JsonResponse({'detail': 'Abonnement introuvable'}, status=404)

        try:
            stripe_warning = None
            if immediate:
                if subscription.stripe_subscription_id:
                    try:
                        stripe.Subscription.delete(subscription.stripe_subscription_id)
                    except stripe_error.StripeError as exc:
                        human = getattr(exc, 'user_message', None) or str(exc)
                        stripe_warning = f"Stripe n’a pas confirmé la suppression ({human})."
                        logger.warning(
                            "AdminSubscriptionCancel immediate Stripe error for %s: %s",
                            subscription.stripe_subscription_id,
                            exc
                        )
                subscription.status = 'canceled'
                subscription.cancel_at_period_end = False
                subscription.current_period_end = timezone.now()
                subscription.save(update_fields=['status', 'cancel_at_period_end', 'current_period_end', 'updated_at'])
                message = "Abonnement résilié immédiatement."
            else:
                if not subscription.cancel_subscription():
                    stripe_warning = (
                        "Impossible de synchroniser l’annulation avec Stripe. "
                        "L’accès a été stoppé côté OptiTAB, pensez à vérifier côté Stripe."
                    )
                    logger.warning(
                        "AdminSubscriptionCancel schedule fallback for sub %s (stripe_id=%s)",
                        subscription.id,
                        subscription.stripe_subscription_id
                    )
                    # Fallback: marquer localement comme annulé à la fin de période
                    if not subscription.cancel_at_period_end:
                        subscription.cancel_at_period_end = True
                    if not subscription.current_period_end:
                        subscription.current_period_end = timezone.now()
                    if subscription.current_period_end <= timezone.now():
                        subscription.status = 'canceled'
                    subscription.save(update_fields=['cancel_at_period_end', 'current_period_end', 'status', 'updated_at'])
                else:
                    subscription.refresh_from_db()
                message = "Annulation programmée à la fin de la période en cours."
        except Exception as exc:
            logger.error(f"AdminSubscriptionCancel error for sub {subscription.id}: {exc}")
            return JsonResponse({'detail': 'Erreur lors de la résiliation.'}, status=500)

        return JsonResponse({
            'success': True,
            'message': message,
             'stripe_warning': stripe_warning,
            'subscription': {
                'id': subscription.id,
                'status': subscription.status,
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'current_period_end': subscription.current_period_end.isoformat() if subscription.current_period_end else None,
            }
        })

@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """Webhook pour gérer les événements Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    if not sig_header:
        logger.warning("Stripe webhook: signature manquante (path=%s)", request.path)

    try:
        event = _construct_stripe_event(payload, sig_header)
    except ValueError as exc:
        logger.warning("Stripe webhook: payload invalide (path=%s): %s", request.path, exc)
        return HttpResponse(status=400)
    except stripe_error.SignatureVerificationError as exc:
        logger.warning("Stripe webhook: signature invalide (path=%s): %s", request.path, exc)
        return HttpResponse(status=400)

    try:
        event_type = event.get('type')
        event_id = event.get('id')
    except Exception:
        try:
            event_type = event['type']
        except Exception:
            event_type = None
        try:
            event_id = event['id']
        except Exception:
            event_id = None
    
    # Gérer les différents types d'événements
    if event_type == 'checkout.session.completed':
        session = event['data']['object']
        # Si la session est un abonnement
        if session.get('subscription'):
            handle_checkout_session_completed(session)
        else:
            handle_checkout_session_payment_completed(session)
    elif event_type == 'checkout.session.expired':
        session = event['data']['object']
        customer_id = session.get('customer')
        if customer_id:
            _clear_customer_temp_invoice_custom_fields(customer_id)

    elif event_type == 'invoice.created':
        handle_invoice_created(event['data']['object'])
    
    elif event_type == 'invoice.payment_succeeded':
        handle_payment_succeeded(event['data']['object'])
    
    elif event_type == 'invoice.payment_failed':
        handle_payment_failed(event['data']['object'])
    
    elif event_type == 'customer.subscription.updated':
        handle_subscription_updated(event['data']['object'])
    
    elif event_type == 'customer.subscription.deleted':
        handle_subscription_deleted(event['data']['object'])
    
    elif event_type == 'charge.refunded':
        logger.info("Stripe webhook: refund event received (type=%s, id=%s)", event_type, event_id)
        handle_charge_refunded(event['data']['object'])
    elif event_type in (
        'refund.created',
        'refund.updated',
        'charge.refund.created',
        'charge.refund.updated',
    ):
        logger.info("Stripe webhook: refund event received (type=%s, id=%s)", event_type, event_id)
        handle_refund_event(event['data']['object'])
    
    return HttpResponse(status=200)

