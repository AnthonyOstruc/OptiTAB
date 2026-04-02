"""
Service centralisé pour construire le statut d'abonnement d'un utilisateur.
Refactorisé pour être DRY, simple et maintenable.
"""
import logging
from datetime import datetime

from django.utils import timezone

from .models import AccessPass, PaymentHistory, SubscriptionPlan, UserSubscription
from .helpers import (
    _build_plan_payload,
    _extract_price_from_stripe_subscription,
    _from_timestamp,
    _is_stripe_subscription_active,
    _map_stripe_status,
)
from .stripe_services import (
    _build_gifted_subscriptions_from_stripe,
    _list_stripe_subscriptions,
    _refresh_subscription_from_snapshot,
    _refresh_subscription_from_stripe,
)
from .pass_access import (
    REFUNDED_STATUSES,
    get_valid_active_passes_for_user,
    sync_refunded_passes,
)
from .permissions import (
    get_manual_access_levels,
    get_manual_access_window_status,
    has_global_complimentary_access,
    user_has_any_manual_access,
)
from pays.models import Niveau

logger = logging.getLogger(__name__)


# =============================================================================
# Helpers de sérialisation (DRY)
# =============================================================================

def serialize_niveau(niveau_obj):
    """Sérialise un objet Niveau en dict. Retourne None si invalide."""
    if not niveau_obj:
        return None
    pays = getattr(niveau_obj, 'pays', None)
    return {
        'id': niveau_obj.id,
        'nom': niveau_obj.nom,
        'pays': {
            'id': pays.id,
            'nom': pays.nom,
            'drapeau_emoji': getattr(pays, 'drapeau_emoji', None),
        } if pays else None
    }


def serialize_beneficiary(user):
    """Sérialise un utilisateur bénéficiaire."""
    if not user:
        return None
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }


def iso_or_none(dt):
    """Convertit une datetime en ISO string, ou None."""
    if not dt:
        return None
    return dt.isoformat() if hasattr(dt, 'isoformat') else str(dt)


def is_period_expired(period_end):
    """Vérifie si une période est expirée."""
    if not period_end:
        return False
    try:
        if isinstance(period_end, str):
            period_end = datetime.fromisoformat(period_end.replace('Z', '+00:00'))
        if period_end.tzinfo is None:
            period_end = period_end.replace(tzinfo=timezone.utc)
        return period_end < timezone.now()
    except Exception:
        return False


# =============================================================================
# Collecteur de niveaux débloqués
# =============================================================================


class UnlockedLevelsCollector:
    """Collecte les niveaux débloqués de manière unique."""
    
    def __init__(self):
        self._levels = {}
    
    def add(self, niveau_payload):
        """Ajoute un niveau si valide et non déjà présent."""
        if not niveau_payload:
            return
        level_id = niveau_payload.get('id')
        if level_id is not None:
            self._levels[level_id] = niveau_payload
    
    def to_list(self):
        """Retourne la liste des niveaux uniques."""
        return list(self._levels.values())


# =============================================================================
# Constructeur de payload d'abonnement
# =============================================================================

def build_subscription_payload(sub, stripe_snapshot=None, user_id=None):
    """
    Construit le payload d'un abonnement depuis un UserSubscription local
    et optionnellement un snapshot Stripe.
    """
    plan = getattr(sub, 'plan', None)
    niveau_obj = getattr(sub, 'niveau_pays', None)
    
    stripe_price = _extract_price_from_stripe_subscription(stripe_snapshot)
    plan_payload = _build_plan_payload(plan, stripe_price, stripe_snapshot)
    
    # Déterminer si c'est un cadeau reçu
    metadata = (stripe_snapshot.get('metadata') or {}) if stripe_snapshot else {}
    payer_id = metadata.get('payer_user_id')
    is_gift = bool(payer_id and user_id and str(payer_id) != str(user_id))
    
    return {
        'id': sub.id,
        'status': sub.status,
        'is_active': sub.is_active,
        'is_trial': sub.is_trial,
        'is_gift_received': is_gift,
        'days_remaining_trial': sub.days_remaining_trial,
        'current_period_start': iso_or_none(sub.current_period_start),
        'current_period_end': iso_or_none(sub.current_period_end),
        'trial_end': iso_or_none(sub.trial_end),
        'cancel_at_period_end': bool(sub.cancel_at_period_end),
        'stripe_subscription_id': sub.stripe_subscription_id,
        'plan': plan_payload,
        'niveau': serialize_niveau(niveau_obj),
        'started_at': iso_or_none(sub.created_at),
    }


def build_stripe_only_subscription_payload(stripe_sub, user_id=None):
    """
    Construit le payload d'un abonnement Stripe sans record local.
    """
    metadata = stripe_sub.get('metadata') or {}
    
    # Récupérer le niveau depuis metadata
    niveau_payload = None
    niveau_id = metadata.get('niveau_pays_id')
    if niveau_id:
        try:
            niveau_obj = Niveau.objects.select_related('pays').get(id=int(niveau_id))
            niveau_payload = serialize_niveau(niveau_obj)
        except (Niveau.DoesNotExist, ValueError, TypeError):
            pass
    
    # Récupérer le plan
    plan_obj = _resolve_plan_from_stripe(stripe_sub, metadata)
    stripe_price = _extract_price_from_stripe_subscription(stripe_sub)
    plan_payload = _build_plan_payload(plan_obj, stripe_price, stripe_sub)
    
    # Dates
    status = _map_stripe_status(stripe_sub.get('status'))
    start_dt = _from_timestamp(stripe_sub.get('current_period_start'))
    end_dt = _from_timestamp(stripe_sub.get('current_period_end'))
    trial_dt = _from_timestamp(stripe_sub.get('trial_end'))
    started_dt = _from_timestamp(stripe_sub.get('start_date')) or start_dt
    
    # Cadeau
    payer_id = metadata.get('payer_user_id')
    is_gift = bool(payer_id and user_id and str(payer_id) != str(user_id))
    
    return {
        'id': None,
        'status': status,
        'is_active': _is_stripe_subscription_active(stripe_sub),
        'is_trial': status == 'trialing',
        'is_gift_received': is_gift,
        'days_remaining_trial': 0,
        'current_period_start': iso_or_none(start_dt),
        'current_period_end': iso_or_none(end_dt),
        'trial_end': iso_or_none(trial_dt),
        'cancel_at_period_end': bool(stripe_sub.get('cancel_at_period_end')),
        'stripe_subscription_id': stripe_sub.get('id'),
        'plan': plan_payload,
        'niveau': niveau_payload,
        'started_at': iso_or_none(started_dt),
    }


def _resolve_plan_from_stripe(stripe_sub, metadata):
    """Résout le plan local depuis un abonnement Stripe."""
    plan_id = metadata.get('plan_id')
    if plan_id:
        try:
            return SubscriptionPlan.objects.filter(id=int(plan_id)).first()
        except (TypeError, ValueError):
            pass
    
    # Fallback: chercher par stripe_price_id
    try:
        items = stripe_sub.get('items', {}).get('data', [])
        if items:
            price_id = items[0].get('price', {}).get('id')
            if price_id:
                return SubscriptionPlan.objects.filter(stripe_price_id=price_id).first()
    except Exception:
        pass
    
    return None


# =============================================================================
# Constructeur de payload de pass
# =============================================================================

def build_pass_payload(access_pass, user):
    """Construit le payload d'un pass d'accès."""
    plan = access_pass.plan
    
    # Récupérer le niveau depuis PaymentHistory
    niveau_payload = None
    payment_intent_id = access_pass.stripe_payment_intent_id
    payment = None
    if payment_intent_id:
        payment = (
            PaymentHistory.objects.filter(
                stripe_payment_intent_id=payment_intent_id,
                plan_mode='one_time',
            )
            .select_related('niveau_pays', 'niveau_pays__pays')
            .first()
        )

    if payment and payment.niveau_pays:
        niveau_payload = serialize_niveau(payment.niveau_pays)
    elif payment_intent_id:
        logger.warning(
            "Pass level unresolved (pass_id=%s, payment_intent=%s, payment_found=%s, has_niveau=%s)",
            access_pass.id,
            payment_intent_id,
            bool(payment),
            bool(getattr(payment, 'niveau_pays_id', None)),
        )
    
    return {
        'id': access_pass.id,
        'plan_name': plan.name if plan else 'Pass',
        'plan_price': float(plan.price) if plan and plan.price else None,
        'plan_billing_period': plan.billing_period if plan else None,
        'stripe_price_id': plan.stripe_price_id if plan else None,
        'starts_at': iso_or_none(access_pass.starts_at),
        'ends_at': iso_or_none(access_pass.ends_at),
        'is_active': access_pass.is_active,
        'is_revoked': access_pass.is_revoked,
        'revoked_at': iso_or_none(access_pass.revoked_at),
        'niveau': niveau_payload,
    }


def build_gifted_pass_payload(access_pass, payment):
    """Construit le payload d'un pass offert."""
    plan = access_pass.plan
    niveau_payload = serialize_niveau(payment.niveau_pays) if payment.niveau_pays else None
    
    return {
        'id': access_pass.id,
        'plan_name': plan.name if plan else payment.plan_name,
        'plan_price': float(plan.price) if plan and plan.price else float(payment.amount),
        'starts_at': iso_or_none(access_pass.starts_at),
        'ends_at': iso_or_none(access_pass.ends_at),
        'is_active': access_pass.is_active,
        'is_revoked': access_pass.is_revoked,
        'revoked_at': iso_or_none(access_pass.revoked_at),
        'niveau': niveau_payload,
        'beneficiary': serialize_beneficiary(access_pass.user),
        'cancel_at_period_end': False,
    }


# =============================================================================
# Fonction principale
# =============================================================================

def build_subscription_status(user):
    """
    Construit le statut complet d'abonnement d'un utilisateur.
    Structure unifiée pour exposer l'état d'accès.
    """
    now = timezone.now()
    user_id = user.id
    manual_levels = get_manual_access_levels(user)
    manual_levels_payload = [serialize_niveau(level) for level in manual_levels]
    manual_access_starts_at = iso_or_none(
        getattr(user, 'complimentary_access_starts_at', None)
    )
    manual_access_ends_at = iso_or_none(
        getattr(user, 'complimentary_access_ends_at', None)
    )
    manual_access_window_status = get_manual_access_window_status(user, now=now)
    has_manual_access_global = has_global_complimentary_access(user)
    has_manual_access = user_has_any_manual_access(user)
    
    # Initialisation de la réponse
    response = {
        'has_subscription': False,
        'status': 'none',
        'is_active': False,
        'has_active_pass': False,
        'has_manual_access': has_manual_access,
        'has_manual_access_global': has_manual_access_global,
        'manual_access_levels': manual_levels_payload,
        'manual_access_starts_at': manual_access_starts_at,
        'manual_access_ends_at': manual_access_ends_at,
        'manual_access_window_status': manual_access_window_status,
        'manual_access_scope': (
            'global'
            if has_manual_access_global
            else ('levels' if manual_levels_payload else 'none')
        ),
    }
    
    levels = UnlockedLevelsCollector()
    if has_manual_access:
        for manual_level in manual_levels_payload:
            levels.add(manual_level)

    subscriptions_payload = []
    primary_subscription = None
    processed_stripe_ids = set()
    
    # --- 1. Charger les données Stripe ---
    stripe_subscriptions = _list_stripe_subscriptions(user)
    gifted_subscriptions = _build_gifted_subscriptions_from_stripe(stripe_subscriptions, user)
    
    # Filtrer les abonnements Stripe pour cet utilisateur uniquement
    stripe_subscriptions = [
        s for s in stripe_subscriptions
        if not (s.get('metadata') or {}).get('user_id') 
        or str((s.get('metadata') or {}).get('user_id')) == str(user_id)
    ]
    
    stripe_lookup = {s.get('id'): s for s in stripe_subscriptions if s.get('id')}
    
    # --- 2. Traiter les abonnements locaux ---
    local_subs = UserSubscription.objects.filter(user=user).select_related(
        'plan', 'niveau_pays', 'niveau_pays__pays'
    ).order_by('-created_at')
    
    for sub in local_subs:
        stripe_snapshot = stripe_lookup.get(sub.stripe_subscription_id)
        
        # Synchroniser avec Stripe
        if stripe_snapshot:
            sub = _refresh_subscription_from_snapshot(sub, stripe_snapshot)
        elif sub.stripe_subscription_id:
            sub = _refresh_subscription_from_stripe(sub)
        else:
            # Pas de stripe_subscription_id -> marquer comme annulé
            if sub.status != 'canceled':
                sub.status = 'canceled'
                sub.save(update_fields=['status', 'updated_at'])
        
        if sub.stripe_subscription_id:
            processed_stripe_ids.add(sub.stripe_subscription_id)
        
        # Construire le payload
        payload = build_subscription_payload(sub, stripe_snapshot, user_id)
        subscriptions_payload.append(payload)
        
        # Ajouter le niveau si actif et non expiré
        if payload['is_active'] and not is_period_expired(payload['current_period_end']):
            levels.add(payload['niveau'])
        
        # Déterminer l'abonnement principal
        if primary_subscription is None:
            primary_subscription = payload
        elif not primary_subscription['is_active'] and payload['is_active']:
            primary_subscription = payload
    
    # --- 3. Traiter les abonnements Stripe sans record local ---
    for stripe_sub in stripe_subscriptions:
        stripe_id = stripe_sub.get('id')
        if not stripe_id or stripe_id in processed_stripe_ids:
            continue
        
        payload = build_stripe_only_subscription_payload(stripe_sub, user_id)
        subscriptions_payload.append(payload)
        
        if payload['is_active'] and not is_period_expired(payload['current_period_end']):
            levels.add(payload['niveau'])
        
        if primary_subscription is None:
            primary_subscription = payload
        elif not primary_subscription['is_active'] and payload['is_active']:
            primary_subscription = payload
    
    # --- 4. Mettre à jour la réponse avec l'abonnement principal ---
    if subscriptions_payload:
        response['has_subscription'] = True
    
    if primary_subscription:
        plan = primary_subscription.get('plan') or {}
        response.update({
            'has_subscription': True,
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
            'plan_name': plan.get('name', 'Plan actuel'),
            'plan_id': plan.get('id'),
            'plan_type': plan.get('plan_type'),
            'plan_mode': plan.get('mode'),
            'plan_billing_period': plan.get('billing_period'),
            'plan_price': plan.get('price'),
            'plan_stripe_price_id': plan.get('stripe_price_id'),
            'plan_currency': plan.get('currency', 'EUR'),
            'features': plan.get('features', []),
        })
    elif subscriptions_payload:
        # Fallback: utiliser le premier abonnement (même inactif)
        fallback = subscriptions_payload[0]
        plan = fallback.get('plan') or {}
        response.update({
            'has_subscription': True,
            'status': fallback['status'],
            'is_active': False,
            'is_trial': fallback['is_trial'],
            'subscription_niveau': fallback['niveau'],
            'started_at': fallback.get('started_at'),
            'plan_name': plan.get('name', 'Plan actuel'),
            'plan_id': plan.get('id'),
            'plan_type': plan.get('plan_type'),
            'plan_mode': plan.get('mode'),
            'plan_billing_period': plan.get('billing_period'),
            'plan_price': plan.get('price'),
            'plan_stripe_price_id': plan.get('stripe_price_id'),
            'plan_currency': plan.get('currency', 'EUR'),
            'features': plan.get('features', []),
        })
    
    response['subscriptions'] = subscriptions_payload
    
    # --- 5. Traiter les passes actifs ---
    active_passes = get_valid_active_passes_for_user(user, now=now)

    passes_payload = []
    for access_pass in active_passes:
        payload = build_pass_payload(access_pass, user)
        passes_payload.append(payload)
        levels.add(payload['niveau'])
    
    response['active_passes'] = passes_payload
    response['has_active_pass'] = len(passes_payload) > 0
    
    # Rétrocompatibilité: premier pass dans anciens champs
    if passes_payload:
        first = passes_payload[0]
        response.update({
            'active_pass_plan': first['plan_name'],
            'active_pass_ends_at': first['ends_at'],
            'active_pass_price_id': first['stripe_price_id'],
            'active_pass_price': first['plan_price'],
            'active_pass_billing_period': first['plan_billing_period'],
            'pass_niveau': first['niveau'],
        })
    
    # --- 6. Passes offerts par ce parent ---
    gifted_passes = []
    parent_payments = PaymentHistory.objects.filter(
        user=user, plan_mode='one_time', period_end__gt=now
    ).exclude(
        status__in=REFUNDED_STATUSES
    ).select_related('niveau_pays', 'niveau_pays__pays')

    payment_intent_ids = [
        payment.stripe_payment_intent_id
        for payment in parent_payments
        if payment.stripe_payment_intent_id
    ]
    candidate_passes = list(
        AccessPass.objects.filter(
            stripe_payment_intent_id__in=payment_intent_ids,
            is_revoked=False,
            ends_at__gt=now,
        )
        .exclude(user=user)
        .select_related('user', 'plan')
    )
    valid_passes = sync_refunded_passes(candidate_passes, max_stripe_checks=3)
    valid_pass_by_intent = {
        access_pass.stripe_payment_intent_id: access_pass
        for access_pass in valid_passes
        if access_pass.stripe_payment_intent_id
    }

    for payment in parent_payments:
        access_pass = valid_pass_by_intent.get(payment.stripe_payment_intent_id)
        if access_pass:
            gifted_passes.append(build_gifted_pass_payload(access_pass, payment))
    
    response['gifted_passes'] = gifted_passes
    
    # --- 7. Finalisation ---
    response['unlocked_levels'] = levels.to_list()
    response['gifted_subscriptions'] = gifted_subscriptions
    
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
