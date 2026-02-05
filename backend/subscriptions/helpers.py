import logging
from datetime import datetime, timezone as dt_timezone
from functools import lru_cache

from django.utils import timezone

from pays.models import Niveau

logger = logging.getLogger(__name__)


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
        amount = invoice.get('amount_paid') or invoice.get('total')
        if amount is not None:
            return amount / 100.0
    return None


def _extract_stripe_amount(source, *keys):
    """Extrait un montant depuis un objet Stripe (convertit centimes → euros)."""
    for key in keys:
        amount = source.get(key)
        if amount is not None:
            return amount / 100.0
    return None


def _extract_stripe_currency(source):
    """Extrait la devise depuis un objet Stripe (en majuscules)."""
    currency = source.get('currency')
    return currency.upper() if currency else None


def _build_plan_payload(plan_obj=None, stripe_price=None, stripe_subscription=None):
    """Construit le payload d'un plan depuis les sources locales et Stripe."""
    payload = _init_plan_payload_from_local(plan_obj)
    
    if stripe_price:
        _enrich_payload_from_stripe_price(payload, stripe_price)
    
    stripe_plan = (stripe_subscription or {}).get('plan') or {}
    if stripe_plan:
        _enrich_payload_from_stripe_plan(payload, stripe_plan)

    if stripe_subscription:
        _enrich_payload_from_subscription(payload, stripe_subscription)
    
    # Valeurs par défaut finales
    payload.setdefault('name', 'Plan Stripe' if stripe_price else 'Plan actuel')
    payload.setdefault('currency', 'EUR')
    payload.setdefault('mode', 'subscription')
    
    return payload


def _init_plan_payload_from_local(plan_obj):
    """Initialise le payload depuis l'objet plan local."""
    return {
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


def _enrich_payload_from_stripe_price(payload, stripe_price):
    """Enrichit le payload avec les données du Price Stripe."""
    payload['stripe_price_id'] = stripe_price.get('id') or payload.get('stripe_price_id')
    
    amount = _extract_stripe_amount(stripe_price, 'unit_amount', 'amount')
    if amount is not None:
        payload['price'] = amount
    
    currency = _extract_stripe_currency(stripe_price)
    if currency:
        payload['currency'] = currency
    
    # Nom du plan
    nickname = stripe_price.get('nickname')
    if nickname:
        payload['name'] = nickname
    elif not payload.get('name'):
        product = stripe_price.get('product')
        if isinstance(product, dict):
            payload['name'] = product.get('name')
        elif product:
            payload['name'] = str(product)
    
    # Période de facturation
    recurring = stripe_price.get('recurring') or {}
    interval = recurring.get('interval') or stripe_price.get('interval')
    if interval:
        payload['billing_period'] = interval
    
    # Mode
    if stripe_price.get('type') == 'one_time':
        payload['mode'] = 'one_time'
    elif not payload.get('mode'):
        payload['mode'] = 'subscription'


def _enrich_payload_from_stripe_plan(payload, stripe_plan):
    """Enrichit le payload avec les données du Plan Stripe (legacy)."""
    # Nom
    nickname = stripe_plan.get('nickname')
    product = stripe_plan.get('product')
    product_name = product.get('name', '') if isinstance(product, dict) else (product or '')
    label = nickname or product_name
    if label:
        payload['name'] = label
    
    # Prix et devise
    amount = _extract_stripe_amount(stripe_plan, 'amount')
    if amount is not None:
        payload['price'] = amount
    
    currency = _extract_stripe_currency(stripe_plan)
    if currency:
        payload['currency'] = currency
    
    # Période et mode
    interval = stripe_plan.get('interval')
    if interval:
        payload['billing_period'] = interval
    payload['mode'] = 'subscription'


def _enrich_payload_from_subscription(payload, stripe_subscription):
    """Enrichit le payload avec les données de la Subscription Stripe."""
    effective_amount = _extract_effective_amount(stripe_subscription)
    if effective_amount is not None:
        payload['price'] = effective_amount
    
    invoice = stripe_subscription.get('latest_invoice')
    if isinstance(invoice, dict):
        currency = _extract_stripe_currency(invoice)
        if currency:
            payload['currency'] = currency
    
    if not payload.get('name'):
        plan_nickname = stripe_subscription.get('plan', {}).get('nickname')
        if plan_nickname:
            payload['name'] = plan_nickname


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


def _sync_user_niveau(user, niveau_obj):
    """Aligne user.niveau_pays et user.pays à partir d'un objet Niveau (si nécessaire)."""
    if not user or not niveau_obj:
        return []

    updated_fields = []
    try:
        if getattr(user, 'niveau_pays_id', None) != getattr(niveau_obj, 'id', None):
            user.niveau_pays = niveau_obj
            updated_fields.append('niveau_pays')

        pays_id = getattr(niveau_obj, 'pays_id', None)
        if pays_id is not None and getattr(user, 'pays_id', None) != pays_id:
            user.pays_id = pays_id
            updated_fields.append('pays')

        if updated_fields:
            user.save(update_fields=updated_fields)
    except Exception as exc:
        logger.warning(
            "Impossible de synchroniser le niveau utilisateur (user=%s, niveau=%s): %s",
            getattr(user, 'id', None),
            getattr(niveau_obj, 'id', None),
            exc,
        )
        return []

    return updated_fields


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


__all__ = [
    '_from_timestamp',
    '_stripe_obj_to_dict',
    '_resolve_plan_mode',
    '_extract_price_from_stripe_subscription',
    '_extract_effective_amount',
    '_extract_stripe_amount',
    '_extract_stripe_currency',
    '_build_plan_payload',
    '_resolve_access_days',
    '_format_level_label_from_obj',
    '_fetch_niveau_by_id',
    '_sync_user_niveau',
    '_level_label_from_metadata',
    '_append_level_to_description',
    '_resolve_payment_plan_mode',
    '_resolve_payment_plan_name',
    '_extract_level_from_invoice',
    '_extract_invoice_period',
    '_map_stripe_status',
    '_is_stripe_subscription_active',
]
