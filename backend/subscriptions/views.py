import stripe
try:
    from stripe import error as stripe_error
except ImportError:
    from stripe import _error as stripe_error  # type: ignore[attr-defined]
import json
from functools import lru_cache
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
import logging
from datetime import datetime, timedelta, timezone as dt_timezone

from .models import SubscriptionPlan, UserSubscription, PaymentHistory, AccessPass
from pays.models import Niveau
from django.db import DatabaseError, models
from stripe_config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, SUCCESS_URL, CANCEL_URL, FREE_TRIAL_DAYS
from core.services import EmailService

stripe.api_key = STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

User = get_user_model()


def _from_timestamp(value):
    """Convertit un timestamp Stripe (secondes) en datetime locale aware."""
    if value in (None, '', 0):
        return None
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return None
    dt_utc = datetime.fromtimestamp(ts, tz=dt_timezone.utc)
    try:
        return timezone.localtime(dt_utc)
    except Exception:
        return dt_utc


def _stripe_obj_to_dict(obj):
    if hasattr(obj, 'to_dict_recursive'):
        return obj.to_dict_recursive()
    return obj if isinstance(obj, dict) else {}


def _resolve_plan_mode(plan):
    if not plan:
        return 'subscription'
    mode = getattr(plan, 'plan_mode', None) or getattr(plan, 'mode', None)
    if mode:
        return mode
    access_days = getattr(plan, 'access_days', 0) or 0
    return 'one_time' if access_days > 0 else 'subscription'


def _extract_price_from_stripe_subscription(stripe_sub):
    if not stripe_sub:
        return None
    try:
        items = (stripe_sub.get('items') or {}).get('data') or []
        if items:
            price = items[0].get('price') or {}
            if price:
                return price
    except Exception:
        pass
    legacy_plan = stripe_sub.get('plan')
    if legacy_plan:
        # Normaliser le format pour rester homogène avec Price
        price_payload = dict(legacy_plan)
        price_payload.setdefault('unit_amount', legacy_plan.get('amount'))
        price_payload.setdefault('recurring', {'interval': legacy_plan.get('interval')})
        price_payload.setdefault('type', 'recurring')
        return price_payload
    return None


def _extract_effective_amount(stripe_sub):
    if not stripe_sub:
        return None
    invoice = stripe_sub.get('latest_invoice')
    if isinstance(invoice, str):
        return None
    if isinstance(invoice, dict):
        amount = invoice.get('amount_paid')
        if amount is None:
            amount = invoice.get('total')
        if amount is not None:
            return amount / 100.0
    return None


def _build_plan_payload(plan_obj=None, stripe_price=None, stripe_subscription=None):
    payload = {
        'id': plan_obj.id if plan_obj else None,
        'name': getattr(plan_obj, 'name', None),
        'plan_type': getattr(plan_obj, 'plan_type', None),
        'mode': _resolve_plan_mode(plan_obj) if plan_obj else None,
        'billing_period': getattr(plan_obj, 'billing_period', None),
        'price': float(plan_obj.price) if plan_obj and plan_obj.price is not None else None,
        'currency': getattr(plan_obj, 'currency', 'EUR'),
        'stripe_price_id': getattr(plan_obj, 'stripe_price_id', None),
        'features': plan_obj.features if plan_obj and hasattr(plan_obj, 'features') else [],
    }
    stripe_plan = (stripe_subscription or {}).get('plan') or {}

    if stripe_price:
        payload['stripe_price_id'] = stripe_price.get('id') or payload['stripe_price_id']
        amount = stripe_price.get('unit_amount')
        if amount is None:
            amount = stripe_price.get('amount')
        if amount is not None:
            payload['price'] = (amount or 0) / 100.0
        currency = stripe_price.get('currency')
        if currency:
            payload['currency'] = currency.upper()
        nickname = stripe_price.get('nickname')
        if nickname:
            payload['name'] = nickname
        elif not payload['name']:
            product_label = stripe_price.get('product')
            if isinstance(product_label, dict):
                payload['name'] = product_label.get('name') or payload['name']
            elif product_label:
                payload['name'] = str(product_label)
        recurring = stripe_price.get('recurring') or {}
        interval = recurring.get('interval') or stripe_price.get('interval')
        if interval:
            payload['billing_period'] = interval
        price_type = stripe_price.get('type')
        if price_type == 'one_time':
            payload['mode'] = 'one_time'
        elif payload['mode'] is None:
            payload['mode'] = 'subscription'
    if stripe_plan:
        nickname = stripe_plan.get('nickname')
        product = stripe_plan.get('product')
        product_name = ''
        if isinstance(product, dict):
            product_name = product.get('name', '')
        elif isinstance(product, str):
            product_name = product
        label = nickname or product_name
        if label:
            payload['name'] = label
        amount = stripe_plan.get('amount')
        if amount is not None:
            payload['price'] = amount / 100.0
        currency = stripe_plan.get('currency')
        if currency:
            payload['currency'] = currency.upper()
        interval = stripe_plan.get('interval')
        if interval:
            payload['billing_period'] = interval
        payload['mode'] = 'subscription'

    if stripe_subscription:
        effective_amount = _extract_effective_amount(stripe_subscription)
        if effective_amount is not None:
            payload['price'] = effective_amount
        invoice = stripe_subscription.get('latest_invoice')
        if isinstance(invoice, dict):
            invoice_currency = invoice.get('currency')
            if invoice_currency:
                payload['currency'] = invoice_currency.upper()
        if not payload['name']:
            product = stripe_subscription.get('plan', {}).get('nickname')
            if product:
                payload['name'] = product
    if not payload['name']:
        payload['name'] = 'Plan Stripe' if stripe_price else 'Plan actuel'
    if not payload['currency']:
        payload['currency'] = 'EUR'
    if not payload['mode']:
        payload['mode'] = 'subscription'
    return payload


def _resolve_access_days(plan, metadata=None):
    """Determine combien de jours d'accès attribuer à un pass."""
    metadata = metadata or {}
    candidates = [
        getattr(plan, 'access_days', None),
        metadata.get('access_days'),
        metadata.get('pass_days'),
        metadata.get('duration_days')
    ]
    for value in candidates:
        if value in (None, '', 0):
            continue
        try:
            days = int(value)
            if days > 0:
                return days
        except (TypeError, ValueError):
            continue
    period = (getattr(plan, 'billing_period', '') or '').lower()
    fallback = {
        'daily': 1,
        'weekly': 7,
        'monthly': 30,
        'yearly': 365
    }.get(period)
    if fallback:
        return fallback
    return 1


def _format_level_label_from_obj(niveau_obj):
    if not niveau_obj:
        return ''
    name = getattr(niveau_obj, 'nom', '') or ''
    pays_obj = getattr(niveau_obj, 'pays', None)
    pays_name = getattr(pays_obj, 'nom', '') if pays_obj else ''
    if name and pays_name:
        return f"{name} · {pays_name}"
    return name or pays_name or ''


@lru_cache(maxsize=256)
def _fetch_niveau_by_id(niveau_id):
    if not niveau_id:
        return None
    try:
        return Niveau.objects.select_related('pays').get(id=int(niveau_id))
    except (ValueError, Niveau.DoesNotExist):
        return None


def _level_label_from_metadata(metadata):
    if not metadata:
        return ''
    label = metadata.get('niveau_label')
    if label:
        return label
    niveau_id = metadata.get('niveau_pays_id')
    niveau_obj = _fetch_niveau_by_id(niveau_id) if niveau_id else None
    return _format_level_label_from_obj(niveau_obj)


def _append_level_to_description(description, level_label, include_hint=False):
    if include_hint and level_label:
        return f"{description} · Niveau: {level_label}"
    return description


def _resolve_payment_plan_mode(payment):
    stored_mode = (getattr(payment, 'plan_mode', '') or '').lower()
    if stored_mode in ('subscription', 'one_time', 'payment'):
        return stored_mode

    if getattr(payment, 'stripe_invoice_id', None):
        return 'subscription'

    description = (payment.description or '').lower()
    if 'paiement pour' in description:
        return 'subscription'
    if 'pass' in description:
        return 'one_time'
    return 'payment'


def _resolve_payment_plan_name(payment, plan_mode):
    stored_name = (getattr(payment, 'plan_name', '') or '').strip()
    if stored_name:
        return stored_name

    description = payment.description or ''
    normalized = description.lower()
    if plan_mode == 'subscription':
        marker = 'paiement pour'
        if marker in normalized:
            idx = normalized.index(marker) + len(marker)
            return description[idx:].strip(' .:-–—')
    elif plan_mode == 'one_time':
        marker = 'pass'
        if marker in normalized:
            idx = normalized.index(marker) + len(marker)
            return description[idx:].strip(' .:-–—()')
    return description.strip()


def _extract_level_from_invoice(invoice):
    """Extraire le niveau depuis les metadata invoice ou les lignes."""
    if not invoice:
        return '', None

    sources = []
    metadata = invoice.get('metadata') or {}
    if metadata:
        sources.append(metadata)

    lines = (invoice.get('lines') or {}).get('data') or []
    for line in lines:
        line_meta = line.get('metadata') or {}
        if line_meta:
            sources.append(line_meta)

    for source in sources:
        niveau_id = source.get('niveau_pays_id')
        niveau_obj = _fetch_niveau_by_id(niveau_id) if niveau_id else None
        level_label = source.get('niveau_label')
        if not level_label and niveau_obj:
            level_label = _format_level_label_from_obj(niveau_obj)
        if level_label or niveau_obj:
            return level_label or '', niveau_obj

    return '', None


def _extract_invoice_period(invoice):
    if not invoice:
        return None, None
    lines = (invoice.get('lines') or {}).get('data') or []
    for line in lines:
        period = line.get('period') or {}
        start = _from_timestamp(period.get('start'))
        end = _from_timestamp(period.get('end'))
        if start or end:
            return start, end
    overall_start = _from_timestamp(invoice.get('period_start'))
    overall_end = _from_timestamp(invoice.get('period_end'))
    return overall_start, overall_end


def _hydrate_payment_history_invoice(payment_history):
    """Assure la présence des URLs de facture en rafraîchissant depuis Stripe si nécessaire."""
    if payment_history.invoice_pdf_url and payment_history.hosted_invoice_url:
        return payment_history.invoice_pdf_url, payment_history.hosted_invoice_url

    invoice_id = payment_history.stripe_invoice_id
    if not invoice_id:
        payment_intent_id = payment_history.stripe_payment_intent_id
        latest_charge_id = None
        if payment_intent_id:
            try:
                pi = stripe.PaymentIntent.retrieve(payment_intent_id, expand=['invoice'])
                latest_charge_id = pi.get('latest_charge') or ''
                invoice_ref = pi.get('invoice')
                if invoice_ref:
                    if isinstance(invoice_ref, str):
                        invoice_data = stripe.Invoice.retrieve(invoice_ref)
                    else:
                        invoice_data = invoice_ref
                    invoice_id = invoice_data.get('id')
                    payment_history.stripe_invoice_id = invoice_id
                    payment_history.save(update_fields=['stripe_invoice_id'])
            except stripe_error.StripeError as exc:
                logger.warning(f"Impossible de récupérer PaymentIntent {payment_intent_id}: {exc}")

            if not invoice_id and latest_charge_id:
                try:
                    charge = stripe.Charge.retrieve(latest_charge_id)
                    receipt_url = charge.get('receipt_url') or ''
                    if receipt_url and not payment_history.hosted_invoice_url:
                        payment_history.hosted_invoice_url = receipt_url
                        payment_history.save(update_fields=['hosted_invoice_url'])
                except stripe_error.StripeError as exc:
                    logger.warning(f"Impossible de récupérer le reçu Stripe {latest_charge_id}: {exc}")

    if not invoice_id:
        return payment_history.invoice_pdf_url, payment_history.hosted_invoice_url

    try:
        invoice = stripe.Invoice.retrieve(invoice_id)
        updated_fields = []
        invoice_pdf = invoice.get('invoice_pdf') or ''
        hosted_url = invoice.get('hosted_invoice_url') or ''
        if invoice_pdf and invoice_pdf != payment_history.invoice_pdf_url:
            payment_history.invoice_pdf_url = invoice_pdf
            updated_fields.append('invoice_pdf_url')
        if hosted_url and hosted_url != payment_history.hosted_invoice_url:
            payment_history.hosted_invoice_url = hosted_url
            updated_fields.append('hosted_invoice_url')
        if updated_fields:
            payment_history.save(update_fields=updated_fields)
    except stripe_error.StripeError as exc:
        logger.warning(f"Impossible de récupérer la facture Stripe {invoice_id}: {exc}")

    return payment_history.invoice_pdf_url, payment_history.hosted_invoice_url


def _map_stripe_status(status):
    mapping = {
        'incomplete': 'past_due',
        'incomplete_expired': 'canceled',
        'trialing': 'trialing',
        'active': 'active',
        'past_due': 'past_due',
        'canceled': 'canceled',
        'unpaid': 'unpaid'
    }
    if not status:
        return 'inactive'
    return mapping.get(status, status)


def _is_stripe_subscription_active(stripe_sub):
    status = stripe_sub.get('status')
    status = _map_stripe_status(status)
    if status in ['active', 'trialing', 'past_due']:
        return True
    if status == 'canceled' and stripe_sub.get('cancel_at_period_end'):
        period_end = stripe_sub.get('current_period_end')
        if period_end:
            period_end_dt = _from_timestamp(period_end)
            if period_end_dt and period_end_dt > timezone.now():
                return True
    return False


def _refresh_subscription_from_stripe(subscription):
    """
    Garantit que les dates clés (début/fin de période, fin d'essai, statut)
    sont renseignées pour un abonnement persisté localement.
    """
    if not subscription or not subscription.stripe_subscription_id:
        return subscription

    needs_period = not subscription.current_period_start or not subscription.current_period_end
    needs_trial = subscription.status == 'trialing' and not subscription.trial_end
    if not needs_period and not needs_trial:
        return subscription

    try:
        stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
    except stripe_error.InvalidRequestError as exc:
        logger.warning(
            "Stripe subscription %s introuvable pour hydratation: %s",
            subscription.stripe_subscription_id,
            exc,
        )
        return subscription
    except stripe_error.StripeError as exc:
        logger.warning(
            "Impossible de rafraîchir l'abonnement Stripe %s: %s",
            subscription.stripe_subscription_id,
            exc,
        )
        return subscription

    updated_fields = []
    start_dt = _from_timestamp(stripe_sub.get('current_period_start'))
    end_dt = _from_timestamp(stripe_sub.get('current_period_end'))
    trial_dt = _from_timestamp(stripe_sub.get('trial_end'))
    mapped_status = _map_stripe_status(stripe_sub.get('status'))
    cancel_flag = bool(stripe_sub.get('cancel_at_period_end'))

    if start_dt and start_dt != subscription.current_period_start:
        subscription.current_period_start = start_dt
        updated_fields.append('current_period_start')
    if end_dt and end_dt != subscription.current_period_end:
        subscription.current_period_end = end_dt
        updated_fields.append('current_period_end')
    if trial_dt and trial_dt != subscription.trial_end:
        subscription.trial_end = trial_dt
        updated_fields.append('trial_end')
    if mapped_status and mapped_status != subscription.status:
        subscription.status = mapped_status
        updated_fields.append('status')
    if cancel_flag != subscription.cancel_at_period_end:
        subscription.cancel_at_period_end = cancel_flag
        updated_fields.append('cancel_at_period_end')

    if updated_fields:
        if 'updated_at' not in updated_fields:
            updated_fields.append('updated_at')
        subscription.save(update_fields=updated_fields)

    return subscription


def _get_stripe_customer_id(user):
    try:
        subscription = user.subscription
        if subscription and subscription.stripe_customer_id:
            return subscription.stripe_customer_id
    except Exception:
        pass

    subs_manager = getattr(user, 'subscriptions', None)
    if subs_manager is not None:
        sub = subs_manager.filter(stripe_customer_id__isnull=False).order_by('-created_at').first()
        if sub:
            return sub.stripe_customer_id
    return None


def _create_stripe_customer(user):
    customer = stripe.Customer.create(
        email=user.email,
        name=f"{user.first_name} {user.last_name}",
        metadata={'user_id': user.id}
    )
    return customer.id


def _list_stripe_subscriptions(user, limit=50):
    customer_id = _get_stripe_customer_id(user)
    if not customer_id:
        return []
    try:
        data = stripe.Subscription.list(
            customer=customer_id,
            status='all',
            limit=limit,
            expand=['data.items.data.price', 'data.latest_invoice', 'data.plan.product']
        )
        return list(getattr(data, 'data', []) or [])
    except stripe_error.StripeError as exc:
        logger.warning(f"Unable to list Stripe subscriptions for user {user.id}: {exc}")
        return []

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
                if beneficiary_email.strip().lower() == request.user.email.lower():
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
            
            # Récupérer le plan
            try:
                plan = SubscriptionPlan.objects.get(stripe_price_id=price_id)
            except SubscriptionPlan.DoesNotExist:
                return JsonResponse({'error': 'Plan non trouvé'}, status=404)
            
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

            # Créer ou récupérer le client Stripe (basé sur le payeur, pas le bénéficiaire)
            existing_customer_id = _get_stripe_customer_id(payer_user)
            if existing_customer_id:
                customer_id = existing_customer_id
            else:
                customer_id = _create_stripe_customer(payer_user)
            
            # Créer la session de checkout (abonnement récurrent ou pass unique)
            plan_mode = _resolve_plan_mode(plan)
            is_subscription = (plan_mode == 'subscription')

            # Vérifier si le BÉNÉFICIAIRE a déjà un abonnement pour ce niveau
            if plan_mode == 'subscription':
                has_level_subscription = UserSubscription.objects.filter(
                    user=beneficiary_user,
                    niveau_pays=niveau_obj
                ).filter(
                    models.Q(status__in=['active', 'trialing']) |
                    models.Q(cancel_at_period_end=True, current_period_end__gt=timezone.now())
                ).exists()
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
                metadata['is_gift'] = 'true'
                metadata['beneficiary_email'] = beneficiary_user.email

            create_kwargs = dict(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription' if is_subscription else 'payment',
                success_url=SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=CANCEL_URL,
                metadata=metadata
            )

            if is_subscription:
                subscription_data = {
                    'metadata': metadata
                }
                if FREE_TRIAL_DAYS > 0:
                    subscription_data['trial_period_days'] = FREE_TRIAL_DAYS
                create_kwargs['subscription_data'] = subscription_data

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
                    checkout_session = stripe.checkout.Session.create(**create_kwargs)
                else:
                    raise
            
            return JsonResponse({'checkout_url': checkout_session.url})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def build_subscription_status(user):
    """Structure commune pour exposer l'état d'accès d'un utilisateur."""
    response = {
        'has_subscription': False,
        'status': 'none',
        'is_active': False,
        'has_active_pass': False,
        'has_manual_access': bool(getattr(user, 'has_complimentary_access', False)),
    }

    subscriptions_qs = UserSubscription.objects.filter(user=user).select_related(
        'plan',
        'niveau_pays',
        'niveau_pays__pays'
    ).order_by('-created_at')

    subscriptions_payload = []
    unlocked_levels = []
    primary_subscription = None
    processed_stripe_ids = set()
    stripe_subscriptions = _list_stripe_subscriptions(user)
    stripe_lookup = {
        stripe_sub.get('id'): stripe_sub
        for stripe_sub in stripe_subscriptions
        if stripe_sub.get('id')
    }

    def add_subscription_payload(payload):
        nonlocal primary_subscription
        subscriptions_payload.append(payload)
        if payload.get('is_active') and payload.get('niveau'):
            unlocked_levels.append(payload['niveau'])
        if primary_subscription is None:
            primary_subscription = payload
        elif not primary_subscription.get('is_active') and payload.get('is_active'):
            primary_subscription = payload

    for sub in subscriptions_qs:
        sub = _refresh_subscription_from_stripe(sub)
        plan = getattr(sub, 'plan', None)
        niveau_obj = getattr(sub, 'niveau_pays', None)
        niveau_payload = None
        if niveau_obj:
            niveau_payload = {
                'id': niveau_obj.id,
                'nom': niveau_obj.nom,
                'pays': {
                    'id': niveau_obj.pays.id,
                    'nom': niveau_obj.pays.nom,
                    'drapeau_emoji': getattr(niveau_obj.pays, 'drapeau_emoji', None)
                } if getattr(niveau_obj, 'pays', None) else None
            }

        stripe_snapshot = stripe_lookup.get(sub.stripe_subscription_id)
        if stripe_snapshot and sub.stripe_subscription_id:
            processed_stripe_ids.add(sub.stripe_subscription_id)
        stripe_price = _extract_price_from_stripe_subscription(stripe_snapshot)
        plan_payload = _build_plan_payload(plan, stripe_price, stripe_snapshot)

        sub_payload = {
            'id': sub.id,
            'status': sub.status,
            'is_active': sub.is_active,
            'is_trial': sub.is_trial,
            'days_remaining_trial': sub.days_remaining_trial,
            'current_period_start': sub.current_period_start.isoformat() if sub.current_period_start else None,
            'current_period_end': sub.current_period_end.isoformat() if sub.current_period_end else None,
            'trial_end': sub.trial_end.isoformat() if sub.trial_end else None,
            'cancel_at_period_end': bool(sub.cancel_at_period_end),
            'stripe_subscription_id': sub.stripe_subscription_id,
            'plan': plan_payload,
            'niveau': niveau_payload,
            'started_at': sub.created_at.isoformat() if sub.created_at else None,
        }
        processed_stripe_ids.add(sub.stripe_subscription_id)
        add_subscription_payload(sub_payload)

    for stripe_sub in stripe_subscriptions:
        stripe_id = stripe_sub.get('id')
        if not stripe_id or stripe_id in processed_stripe_ids:
            continue
        metadata = stripe_sub.get('metadata') or {}
        niveau_id = metadata.get('niveau_pays_id')
        niveau_payload = None
        if niveau_id:
            try:
                niveau_obj = Niveau.objects.select_related('pays').get(id=int(niveau_id))
                niveau_payload = {
                    'id': niveau_obj.id,
                    'nom': niveau_obj.nom,
                    'pays': {
                        'id': niveau_obj.pays.id,
                        'nom': niveau_obj.pays.nom,
                        'drapeau_emoji': getattr(niveau_obj.pays, 'drapeau_emoji', None)
                    } if niveau_obj.pays else None
                }
            except Niveau.DoesNotExist:
                niveau_payload = None

        plan_obj = None
        plan_id = metadata.get('plan_id')
        if plan_id:
            try:
                plan_obj = SubscriptionPlan.objects.filter(id=int(plan_id)).first()
            except (TypeError, ValueError):
                plan_obj = None
        if not plan_obj:
            price_id = None
            try:
                items = stripe_sub.get('items', {}).get('data', [])
                if items:
                    price_id = items[0].get('price', {}).get('id')
            except Exception:
                price_id = None
            if price_id:
                plan_obj = SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()

        stripe_price = _extract_price_from_stripe_subscription(stripe_sub)
        plan_payload = _build_plan_payload(plan_obj, stripe_price, stripe_sub)

        status = _map_stripe_status(stripe_sub.get('status'))
        start_dt = _from_timestamp(stripe_sub.get('current_period_start'))
        end_dt = _from_timestamp(stripe_sub.get('current_period_end'))
        trial_dt = _from_timestamp(stripe_sub.get('trial_end'))
        started_dt = _from_timestamp(stripe_sub.get('start_date')) or start_dt
        sub_payload = {
            'id': None,
            'status': status,
            'is_active': _is_stripe_subscription_active(stripe_sub),
            'is_trial': status == 'trialing',
            'days_remaining_trial': 0,
            'current_period_start': start_dt.isoformat() if start_dt else None,
            'current_period_end': end_dt.isoformat() if end_dt else None,
            'trial_end': trial_dt.isoformat() if trial_dt else None,
            'cancel_at_period_end': bool(stripe_sub.get('cancel_at_period_end')),
            'stripe_subscription_id': stripe_id,
            'plan': plan_payload,
            'niveau': niveau_payload,
            'started_at': started_dt.isoformat() if started_dt else None,
        }
        add_subscription_payload(sub_payload)

    if subscriptions_payload and not response['has_subscription']:
        response['has_subscription'] = True

    if primary_subscription:
        primary_plan = primary_subscription.get('plan') or {}
        response.update({
            'has_subscription': True,
            'plan_name': primary_plan.get('name', 'Plan actuel'),
            'plan_id': primary_plan.get('id'),
            'plan_type': primary_plan.get('plan_type'),
            'plan_mode': primary_plan.get('mode'),
            'plan_billing_period': primary_plan.get('billing_period'),
            'plan_price': primary_plan.get('price'),
            'plan_stripe_price_id': primary_plan.get('stripe_price_id'),
            'plan_currency': primary_plan.get('currency', 'EUR'),
            'status': primary_subscription['status'],
            'is_active': primary_subscription['is_active'],
            'is_trial': primary_subscription['is_trial'],
            'days_remaining_trial': primary_subscription['days_remaining_trial'],
            'current_period_start': primary_subscription['current_period_start'],
            'current_period_end': primary_subscription['current_period_end'],
            'trial_end': primary_subscription['trial_end'],
            'cancel_at_period_end': primary_subscription['cancel_at_period_end'],
            'subscription_niveau': primary_subscription['niveau'],
            'started_at': primary_subscription.get('started_at'),
            'features': primary_plan.get('features', []),
        })
    elif subscriptions_payload:
        # Utiliser la première subscription même inactif pour afficher les infos de plan
        fallback = subscriptions_payload[0]
        fallback_plan = fallback.get('plan') or {}
        response.update({
            'has_subscription': True,
            'status': fallback['status'],
            'is_active': False,
            'is_trial': fallback['is_trial'],
            'plan_name': fallback_plan.get('name', 'Plan actuel'),
            'plan_id': fallback_plan.get('id'),
            'plan_type': fallback_plan.get('plan_type'),
            'plan_mode': fallback_plan.get('mode'),
            'plan_billing_period': fallback_plan.get('billing_period'),
            'plan_price': fallback_plan.get('price'),
            'plan_stripe_price_id': fallback_plan.get('stripe_price_id'),
            'plan_currency': fallback_plan.get('currency', 'EUR'),
            'subscription_niveau': fallback['niveau'],
            'started_at': fallback.get('started_at'),
            'features': fallback_plan.get('features', []),
        })

    response['subscriptions'] = subscriptions_payload
    unique_levels = {}

    def _push_level(level_payload):
        if not level_payload:
            return
        level_id = level_payload.get('id')
        if level_id is None:
            return
        unique_levels[level_id] = level_payload

    for level in unlocked_levels:
        if not isinstance(level, dict):
            continue
        _push_level(level)

    response['unlocked_levels'] = list(unique_levels.values())

    active_pass = (
        AccessPass.objects.filter(user=user, ends_at__gt=timezone.now())
        .order_by('-ends_at')
        .first()
    )
    if active_pass:
        pass_plan = getattr(active_pass, 'plan', None)
        niveau_obj = getattr(user, 'niveau_pays', None)
        pass_level = None
        if niveau_obj:
            pass_level = {
                'id': niveau_obj.id,
                'nom': niveau_obj.nom,
                'pays': {
                    'id': getattr(niveau_obj.pays, 'id', None),
                    'nom': getattr(niveau_obj.pays, 'nom', None),
                    'drapeau_emoji': getattr(niveau_obj.pays, 'drapeau_emoji', None)
                } if getattr(niveau_obj, 'pays', None) else None
            }
            _push_level(pass_level)

        response.update({
            'has_active_pass': True,
            'active_pass_plan': pass_plan.name if pass_plan else 'Pass actif',
            'active_pass_ends_at': active_pass.ends_at.isoformat(),
            'active_pass_price_id': getattr(pass_plan, 'stripe_price_id', None) if pass_plan else None,
            'pass_niveau': pass_level
        })
        response['unlocked_levels'] = list(unique_levels.values())

    if response['has_manual_access'] and not response.get('has_subscription'):
        response.setdefault('plan_name', 'Accès manuel')
        response['status'] = 'manual'

    response['has_access'] = bool(
        response.get('is_active')
        or response.get('has_active_pass')
        or response.get('has_manual_access')
    )
    response['can_subscribe'] = True
    return response

class SubscriptionStatusView(APIView):
    """Récupérer le statut d'abonnement de l'utilisateur"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse(build_subscription_status(request.user))


def _sync_payment_history_from_stripe(user, limit=12):
    """
    S'assure que les factures Stripe récentes existent dans PaymentHistory.
    Permet de combler les écarts (par ex. si un webhook n'a pas été reçu).
    """
    try:
        subscription = user.subscription
    except UserSubscription.DoesNotExist:
        subscription = None

    customer_id = getattr(subscription, 'stripe_customer_id', None)
    if not customer_id:
        return 0

    # Préparer une table de correspondance stripe_subscription_id -> UserSubscription
    subscriptions_map = {}
    try:
        subs_qs = (
            UserSubscription.objects
            .filter(user=user, stripe_subscription_id__isnull=False)
            .select_related('plan', 'niveau_pays', 'niveau_pays__pays')
        )
        for sub in subs_qs:
            subscriptions_map[sub.stripe_subscription_id] = sub
    except Exception:
        subs_qs = []

    try:
        total_target = int(limit or 12)
    except (TypeError, ValueError):
        total_target = 12
    total_target = max(1, min(total_target, 500))

    synced = 0
    default_plan_name = getattr(getattr(subscription, 'plan', None), 'name', 'OptiTAB')
    fetched = 0
    starting_after = None

    while fetched < total_target:
        page_limit = min(100, total_target - fetched)
        params = {
            'customer': customer_id,
            'limit': page_limit,
            'expand': ['data.lines']
        }
        if starting_after:
            params['starting_after'] = starting_after

        try:
            stripe_invoices = stripe.Invoice.list(**params)
        except stripe_error.StripeError as exc:
            logger.warning(f"Stripe invoice sync failed for user {user.id}: {exc}")
            break

        data = getattr(stripe_invoices, 'data', None) or []
        if not data:
            break

        for invoice in data:
            invoice_id = invoice.get('id')
            if not invoice_id:
                continue

            payment_intent_id = invoice.get('payment_intent') or f'invoice_{invoice_id}'
            invoice_metadata = invoice.get('metadata') or {}
            stripe_sub_id = invoice.get('subscription')
            linked_subscription = subscriptions_map.get(stripe_sub_id)
            niveau_obj = None
            niveau_id = invoice_metadata.get('niveau_pays_id')
            if niveau_id:
                niveau_obj = _fetch_niveau_by_id(niveau_id)
            level_label = _level_label_from_metadata(invoice_metadata)

            extracted_label, extracted_niveau = _extract_level_from_invoice(invoice)
            if extracted_niveau and not niveau_obj:
                niveau_obj = extracted_niveau
            if extracted_label:
                level_label = extracted_label

            if not level_label:
                niveau_fallback = getattr(linked_subscription, 'niveau_pays', None) or getattr(subscription, 'niveau_pays', None)
                level_label = _format_level_label_from_obj(niveau_fallback)
            plan_source = linked_subscription or subscription
            plan_obj = getattr(plan_source, 'plan', None)
            plan_name = (
                invoice_metadata.get('plan_name') or
                getattr(plan_obj, 'name', None) or
                default_plan_name
            )
            if (not invoice_metadata.get('plan_name')):
                line_description = None
                lines = (invoice.get('lines') or {}).get('data') or []
                if lines:
                    line_description = lines[0].get('description')
                if line_description:
                    cleaned = line_description.split('(')[0]
                    cleaned = cleaned.replace('1 ×', '').strip()
                    if cleaned:
                        plan_name = cleaned
            plan_mode = invoice_metadata.get('plan_mode') or (invoice_metadata.get('mode'))
            if not plan_mode:
                plan_mode = 'subscription' if stripe_sub_id else 'one_time'
            niveau_obj = (
                niveau_obj or
                getattr(linked_subscription, 'niveau_pays', None) or
                getattr(subscription, 'niveau_pays', None)
            )
            if plan_mode == 'one_time':
                base_description = invoice.get('description') or f"Pass {plan_name}"
            else:
                base_description = invoice.get('description') or f"Paiement pour {plan_name}"
            period_start, period_end = _extract_invoice_period(invoice)

            defaults = {
                'stripe_payment_intent_id': payment_intent_id,
                'hosted_invoice_url': (invoice.get('hosted_invoice_url') or ''),
                'invoice_pdf_url': (invoice.get('invoice_pdf') or ''),
                'amount': ((invoice.get('amount_paid') or invoice.get('total') or 0) / 100.0),
                'currency': (invoice.get('currency') or 'EUR').upper(),
                'status': invoice.get('status') or 'paid',
                'description': _append_level_to_description(base_description, level_label),
                'niveau_label': level_label or '',
                'niveau_pays': niveau_obj,
                'plan_name': plan_name or '',
                'plan_mode': plan_mode,
                'period_start': period_start,
                'period_end': period_end,
            }

            payment_history, created = PaymentHistory.objects.get_or_create(
                user=user,
                stripe_invoice_id=invoice_id,
                defaults=defaults
            )

            if created:
                synced += 1
                continue

            niveau_info_available = bool(niveau_id) or bool(level_label)
            updated_fields = []
            for field, value in defaults.items():
                if field == 'niveau_pays' and not niveau_info_available:
                    continue
                if field == 'niveau_label' and not niveau_info_available:
                    continue
                current_value = getattr(payment_history, field)
                if field == 'niveau_pays':
                    current_id = current_value.id if current_value else None
                    value_id = value.id if value else None
                    if current_id != value_id:
                        setattr(payment_history, field, value)
                        updated_fields.append(field)
                    continue
                if current_value != value:
                    setattr(payment_history, field, value)
                    updated_fields.append(field)

            if updated_fields:
                payment_history.save(update_fields=updated_fields)

        fetched += len(data)
        if not getattr(stripe_invoices, 'has_more', False):
            break
        starting_after = data[-1].id

    return synced


class InvoiceListView(APIView):
    """Liste des factures Stripe de l'utilisateur"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_param = (request.GET.get('all', 'false').lower() == 'true')
        try:
            requested_limit = int(request.GET.get('limit', 50))
        except (TypeError, ValueError):
            requested_limit = 50
        requested_limit = max(1, min(requested_limit, 500))
        sync_target = 200 if all_param else max(12, requested_limit)

        # Synchroniser les factures Stripe au cas où le webhook n'aurait pas été reçu
        try:
            _sync_payment_history_from_stripe(request.user, limit=sync_target)
        except Exception as sync_exc:
            logger.warning(f"Unable to sync invoices for user {request.user.id}: {sync_exc}")

        invoices = []
        try:
            qs = PaymentHistory.objects.filter(user=request.user).order_by('-created_at')
            if not all_param:
                qs = qs[:requested_limit]
        except DatabaseError as exc:
            logger.error(f"InvoiceList DB error: {exc}")
            return JsonResponse({
                'detail': 'Factures indisponibles. Assurez-vous d\'avoir appliqué les dernières migrations backend.'
            }, status=503)
        for payment in qs:
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
        return JsonResponse({'invoices': invoices})


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
            if customer_email and customer_email.lower() != (user_email or ''):
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
        return JsonResponse({
            'status': status_payload,
            'has_access': status_payload.get('has_access', False)
        })

class CancelSubscriptionView(APIView):
    """Annuler l'abonnement"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription_id = request.data.get('subscription_id')
        stripe_subscription_id = request.data.get('stripe_subscription_id')
        subscription = None

        if subscription_id:
            try:
                subscription = UserSubscription.objects.get(id=subscription_id, user=request.user)
            except (UserSubscription.DoesNotExist, ValueError):
                subscription = UserSubscription.objects.filter(stripe_subscription_id=subscription_id, user=request.user).first()
                if not subscription and isinstance(subscription_id, str) and subscription_id.startswith('sub_'):
                    stripe_subscription_id = subscription_id

        if not subscription and stripe_subscription_id:
            subscription = UserSubscription.objects.filter(stripe_subscription_id=stripe_subscription_id, user=request.user).first()

        if subscription:
            if subscription.cancel_subscription():
                message = 'Annulation programmée à la fin de la période en cours.'
                return JsonResponse({'success': True, 'message': message})
            return JsonResponse({'error': 'Erreur lors de l\'annulation', 'message': 'Impossible de programmer l\'annulation.'}, status=400)

        if stripe_subscription_id:
            try:
                stripe.Subscription.modify(
                    stripe_subscription_id,
                    cancel_at_period_end=True
                )
                return JsonResponse({'success': True, 'message': 'Annulation programmée à la fin de la période en cours.'})
            except stripe_error.StripeError as exc:
                logger.error(f"Stripe cancel error {stripe_subscription_id}: {exc}")
                return JsonResponse({'error': 'Stripe a refusé l\'annulation', 'message': 'Stripe a refusé l\'annulation.'}, status=400)

        return JsonResponse({'error': 'Abonnement introuvable', 'message': 'Aucun abonnement correspondant trouvé.'}, status=404)

class PlansListView(APIView):
    """Liste des plans disponibles"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
            plans_data = []
            for plan in plans:
                plans_data.append({
                    'id': plan.id,
                    'name': plan.name,
                    'plan_type': plan.plan_type,
                    'mode': _resolve_plan_mode(plan),
                    'billing_period': plan.billing_period,
                    'price': float(plan.price),
                    'stripe_price_id': plan.stripe_price_id,
                    'features': plan.features,
                    'access_days': getattr(plan, 'access_days', None),
                })
            return JsonResponse({'plans': plans_data})
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

def _plan_to_dict(plan):
    return {
        'id': plan.id,
        'name': plan.name,
        'plan_type': plan.plan_type,
        'mode': _resolve_plan_mode(plan),
        'billing_period': plan.billing_period,
        'price': float(plan.price),
        'stripe_price_id': plan.stripe_price_id,
        'features': plan.features,
        'access_days': getattr(plan, 'access_days', None),
        'is_active': plan.is_active,
        'created_at': plan.created_at.isoformat() if plan.created_at else None,
    }

class AdminPlansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_admin(request.user):
            return JsonResponse({'detail': 'Forbidden'}, status=403)
        qs = SubscriptionPlan.objects.all().order_by('-is_active', 'price')
        return JsonResponse({'plans': [_plan_to_dict(p) for p in qs]})

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
            return JsonResponse({'plan': _plan_to_dict(plan)}, status=201)
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
            for field in ['name', 'plan_type', 'billing_period', 'price', 'stripe_price_id', 'is_active']:
                if field in data:
                    setattr(plan, field, data[field])
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
            return JsonResponse({'plan': _plan_to_dict(plan)})
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

            def iso_or_none(dt):
                try:
                    return dt.isoformat() if dt else None
                except Exception:
                    return None

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
                        'current_period_start': iso_or_none(getattr(s, 'current_period_start', None)),
                        'current_period_end': iso_or_none(getattr(s, 'current_period_end', None)),
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
                        is_active = bool(p.ends_at and (p.ends_at > now))
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
                            'starts_at': iso_or_none(getattr(p, 'starts_at', None)),
                            'ends_at': iso_or_none(getattr(p, 'ends_at', None)),
                            'is_active': is_active,
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
                            'current_period_start': iso_or_none(getattr(user, 'date_joined', None)),
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

            def _from_timestamp(value):
                """Convert Stripe timestamp (seconds) to aware UTC datetime."""
                if not value:
                    return None
                try:
                    return datetime.fromtimestamp(value, tz=dt_timezone.utc)
                except Exception:
                    return None

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

                    defaults = {
                        'plan': plan,
                        'stripe_subscription_id': s.id,
                        'stripe_customer_id': s.customer['id'] if isinstance(s.customer, dict) else s.customer,
                        'status': s.status,
                        'current_period_start': _from_timestamp(getattr(s, 'current_period_start', None)),
                        'current_period_end': _from_timestamp(getattr(s, 'current_period_end', None)),
                        'trial_end': _from_timestamp(getattr(s, 'trial_end', None)),
                        'cancel_at_period_end': bool(getattr(s, 'cancel_at_period_end', False)),
                    }

                    obj, was_created = UserSubscription.objects.update_or_create(
                        user=user,
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
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe_error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Gérer les différents types d'événements
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Si la session est un abonnement
        if session.get('subscription'):
            handle_checkout_session_completed(session)
        else:
            handle_checkout_session_payment_completed(session)
    
    elif event['type'] == 'invoice.payment_succeeded':
        handle_payment_succeeded(event['data']['object'])
    
    elif event['type'] == 'invoice.payment_failed':
        handle_payment_failed(event['data']['object'])
    
    elif event['type'] == 'customer.subscription.updated':
        handle_subscription_updated(event['data']['object'])
    
    elif event['type'] == 'customer.subscription.deleted':
        handle_subscription_deleted(event['data']['object'])
    
    return HttpResponse(status=200)

def handle_checkout_session_completed(session):
    """Gérer la completion d'une session de checkout"""
    try:
        user_id = session['metadata']['user_id']
        plan_id = session['metadata']['plan_id']
        niveau_id = session['metadata'].get('niveau_pays_id')
        
        user = User.objects.get(id=user_id)
        plan = SubscriptionPlan.objects.get(id=plan_id)
        niveau_obj = None
        if niveau_id:
            try:
                niveau_obj = Niveau.objects.get(id=niveau_id, est_actif=True)
            except Niveau.DoesNotExist:
                niveau_obj = None
        
        # Récupérer l'abonnement Stripe
        subscription = stripe.Subscription.retrieve(session['subscription'])
        subscription_data = _stripe_obj_to_dict(subscription)
        
        stripe_subscription_id = subscription_data.get('id')
        # Créer ou mettre à jour l'abonnement utilisateur correspondant à cette souscription Stripe
        defaults = {
            'user': user,
            'plan': plan,
            'stripe_customer_id': session.get('customer'),
            'status': subscription_data.get('status', 'active'),
            'current_period_start': _from_timestamp(subscription_data.get('current_period_start')),
            'current_period_end': _from_timestamp(subscription_data.get('current_period_end')),
            'trial_end': _from_timestamp(subscription_data.get('trial_end')),
            'cancel_at_period_end': bool(subscription_data.get('cancel_at_period_end')),
            'niveau_pays': niveau_obj
        }

        user_subscription, created = UserSubscription.objects.get_or_create(
            stripe_subscription_id=stripe_subscription_id,
            defaults=defaults
        )
        
        if not created:
            user_subscription.plan = plan
            user_subscription.user = user
            user_subscription.stripe_customer_id = session.get('customer')
            user_subscription.status = subscription_data.get('status', user_subscription.status)
            user_subscription.current_period_start = _from_timestamp(subscription_data.get('current_period_start'))
            user_subscription.current_period_end = _from_timestamp(subscription_data.get('current_period_end'))
            user_subscription.trial_end = _from_timestamp(subscription_data.get('trial_end'))
            user_subscription.cancel_at_period_end = bool(subscription_data.get('cancel_at_period_end'))
            if niveau_obj:
                user_subscription.niveau_pays = niveau_obj
            user_subscription.save()
        elif niveau_obj and user_subscription.niveau_pays_id != niveau_obj.id:
            user_subscription.niveau_pays = niveau_obj
            user_subscription.save(update_fields=['niveau_pays'])

        if niveau_obj:
            updated_fields = []
            if user.niveau_pays_id != niveau_obj.id:
                user.niveau_pays = niveau_obj
                updated_fields.append('niveau_pays')
            if user.pays_id != niveau_obj.pays_id:
                user.pays_id = niveau_obj.pays_id
                if 'pays' not in updated_fields:
                    updated_fields.append('pays')
            if updated_fields:
                user.save(update_fields=updated_fields)
        
        # Envoyer un email de notification à l'élève si c'est un achat parent → enfant
        metadata = session.get('metadata', {})
        is_gift = metadata.get('is_gift') == 'true'
        payer_user_id = metadata.get('payer_user_id')
        
        if is_gift and payer_user_id:
            try:
                payer = User.objects.get(id=payer_user_id)
                # Notifier l'élève qu'il a reçu un abonnement
                EmailService.send_gift_subscription_notification(
                    recipient=user,
                    gifter=payer,
                    plan=plan,
                    niveau=niveau_obj
                )
                logger.info(f"Email de cadeau d'abonnement envoyé à {user.email} de la part de {payer.email}")
            except User.DoesNotExist:
                logger.warning(f"Payeur {payer_user_id} introuvable pour envoi email cadeau")
            except Exception as email_exc:
                logger.error(f"Erreur envoi email cadeau abonnement: {email_exc}")
        
    except Exception as e:
        logger.error(f"Erreur dans handle_checkout_session_completed: {e}")

def handle_checkout_session_payment_completed(session):
    """Gérer la completion d'une session de checkout en mode paiement unique"""
    try:
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
        if plan_mode != 'one_time':
            plan_mode = _resolve_plan_mode(plan)
            if plan_mode != 'one_time':
                return

        niveau_obj = None
        if niveau_id:
            try:
                niveau_obj = Niveau.objects.get(id=niveau_id, est_actif=True)
            except Niveau.DoesNotExist:
                niveau_obj = None

        # Déterminer la durée d'accès
        days = _resolve_access_days(plan, metadata)
        start = timezone.now()
        ends = start + timedelta(days=days)

        # Créer le pass d'accès
        AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=start,
            ends_at=ends,
            stripe_payment_intent_id=session.get('payment_intent')
        )

        # Journaliser le paiement
        amount_total = session.get('amount_total')  # en cents
        currency = (session.get('currency') or 'eur').upper()
        level_label = _format_level_label_from_obj(niveau_obj)
        if amount_total:
            PaymentHistory.objects.create(
                user=user,
                stripe_payment_intent_id=session.get('payment_intent', ''),
                stripe_invoice_id=session.get('invoice'),
                hosted_invoice_url='',
                invoice_pdf_url='',
                amount=(amount_total / 100.0),
                currency=currency,
                status='succeeded',
                description=_append_level_to_description(f"Pass {plan.name} ({days} jours)", level_label),
                plan_name=plan.name,
                plan_mode='one_time',
                period_start=start,
                period_end=ends,
                niveau_pays=niveau_obj,
                niveau_label=level_label
            )

        if niveau_obj:
            updated_fields = []
            if user.niveau_pays_id != niveau_obj.id:
                user.niveau_pays = niveau_obj
                updated_fields.append('niveau_pays')
            if user.pays_id != niveau_obj.pays_id:
                user.pays_id = niveau_obj.pays_id
                updated_fields.append('pays')
            if updated_fields:
                user.save(update_fields=updated_fields)
        
        # Envoyer un email de notification à l'élève si c'est un achat parent → enfant
        is_gift = metadata.get('is_gift') == 'true'
        payer_user_id = metadata.get('payer_user_id')
        
        if is_gift and payer_user_id:
            try:
                payer = User.objects.get(id=payer_user_id)
                # Notifier l'élève qu'il a reçu un pass
                EmailService.send_gift_subscription_notification(
                    recipient=user,
                    gifter=payer,
                    plan=plan,
                    niveau=niveau_obj
                )
                logger.info(f"Email de cadeau de pass envoyé à {user.email} de la part de {payer.email}")
            except User.DoesNotExist:
                logger.warning(f"Payeur {payer_user_id} introuvable pour envoi email cadeau")
            except Exception as email_exc:
                logger.error(f"Erreur envoi email cadeau pass: {email_exc}")
    except Exception as e:
        logger.error(f"Erreur dans handle_checkout_session_payment_completed: {e}")

def handle_payment_succeeded(invoice):
    """Gérer un paiement réussi"""
    try:
        invoice_id = invoice.get('id')
        if not invoice.get('lines') and invoice_id:
            invoice = stripe.Invoice.retrieve(invoice_id, expand=['lines'])

        subscription_id = invoice['subscription']
        subscription = stripe.Subscription.retrieve(subscription_id)
        subscription_data = _stripe_obj_to_dict(subscription)

        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)
        user_subscription.status = 'active'
        user_subscription.current_period_start = _from_timestamp(subscription_data.get('current_period_start'))
        user_subscription.current_period_end = _from_timestamp(subscription_data.get('current_period_end'))
        user_subscription.cancel_at_period_end = bool(subscription_data.get('cancel_at_period_end', user_subscription.cancel_at_period_end))
        user_subscription.save()

        # Enregistrer le paiement
        level_label = _format_level_label_from_obj(user_subscription.niveau_pays)
        period_start, period_end = _extract_invoice_period(invoice)

        PaymentHistory.objects.create(
            user=user_subscription.user,
            stripe_payment_intent_id=invoice['payment_intent'],
            stripe_invoice_id=invoice.get('id'),
            hosted_invoice_url=invoice.get('hosted_invoice_url', '') or '',
            invoice_pdf_url=invoice.get('invoice_pdf', '') or '',
            amount=invoice['amount_paid'] / 100,  # Stripe utilise les centimes
            currency=invoice['currency'].upper(),
            status='succeeded',
            description=_append_level_to_description(f"Paiement pour {user_subscription.plan.name}", level_label),
            plan_name=user_subscription.plan.name,
            plan_mode=user_subscription.plan.plan_mode or 'subscription',
            period_start=period_start,
            period_end=period_end,
            niveau_pays=user_subscription.niveau_pays,
            niveau_label=level_label
        )
        
    except Exception as e:
        logger.error(f"Erreur dans handle_payment_succeeded: {e}")

def handle_payment_failed(invoice):
    """Gérer un paiement échoué"""
    try:
        subscription_id = invoice['subscription']
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription_id)
        user_subscription.status = 'past_due'
        user_subscription.save()
        
    except Exception as e:
        logger.error(f"Erreur dans handle_payment_failed: {e}")

def handle_subscription_updated(subscription):
    """Gérer la mise à jour d'un abonnement"""
    try:
        subscription = _stripe_obj_to_dict(subscription)
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription['id'])
        user_subscription.status = subscription.get('status', user_subscription.status)
        user_subscription.current_period_start = _from_timestamp(subscription.get('current_period_start'))
        user_subscription.current_period_end = _from_timestamp(subscription.get('current_period_end'))
        user_subscription.cancel_at_period_end = bool(subscription.get('cancel_at_period_end', user_subscription.cancel_at_period_end))
        user_subscription.save()
        
    except Exception as e:
        logger.error(f"Erreur dans handle_subscription_updated: {e}")

def handle_subscription_deleted(subscription):
    """Gérer la suppression d'un abonnement"""
    try:
        subscription = _stripe_obj_to_dict(subscription)
        user_subscription = UserSubscription.objects.get(stripe_subscription_id=subscription['id'])
        user_subscription.status = 'canceled'
        user_subscription.cancel_at_period_end = False
        user_subscription.save()
        
    except Exception as e:
        logger.error(f"Erreur dans handle_subscription_deleted: {e}")
