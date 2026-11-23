from django.utils import timezone
from rest_framework.permissions import BasePermission

from .models import AccessPass, PaymentHistory, UserSubscription
from .pass_access import has_valid_active_pass, sync_refunded_passes


def _normalize_niveau_id(niveau):
    """Return an integer level id when possible, otherwise None."""
    if niveau is None:
        return None
    if isinstance(niveau, int):
        return niveau
    if isinstance(niveau, str):
        try:
            return int(niveau)
        except (TypeError, ValueError):
            return None
    raw_id = getattr(niveau, 'id', None)
    if raw_id is None:
        return None
    try:
        return int(raw_id)
    except (TypeError, ValueError):
        return None


def _normalize_datetime_for_compare(value):
    """Normalize datetimes to timezone-aware values for safe comparisons."""
    if not value:
        return None
    if timezone.is_naive(value):
        try:
            return timezone.make_aware(value, timezone.get_current_timezone())
        except Exception:
            try:
                return timezone.make_aware(value)
            except Exception:
                return value
    return value


def get_content_niveau(content_obj):
    """
    Resolve the educational level for content linked through:
    content -> notion -> theme -> contexte -> niveau.
    """
    notion = getattr(content_obj, 'notion', None)
    theme = getattr(notion, 'theme', None)
    contexte = getattr(theme, 'contexte', None)
    return getattr(contexte, 'niveau', None)


def get_manual_access_levels(user):
    """Return the complimentary levels assigned manually by admin."""
    if not user or not getattr(user, 'id', None):
        return []

    cached = getattr(user, '_manual_access_levels_cache', None)
    if cached is not None:
        return cached

    manager = getattr(user, 'complimentary_access_levels', None)
    if manager is None:
        levels = []
    else:
        levels = list(manager.select_related('pays').all())

    setattr(user, '_manual_access_levels_cache', levels)
    return levels


def get_manual_access_level_ids(user):
    """Return complimentary level ids as a set[int]."""
    return {
        level.id
        for level in get_manual_access_levels(user)
        if getattr(level, 'id', None) is not None
    }


def get_manual_access_window_status(user, now=None):
    """
    Return manual access window status:
    - scheduled: start date is set and in the future
    - expired: end date is set and already passed
    - active: no boundary or currently inside the configured range
    """
    if not user:
        return 'inactive'

    current_dt = _normalize_datetime_for_compare(now or timezone.now())
    starts_at = _normalize_datetime_for_compare(
        getattr(user, 'complimentary_access_starts_at', None)
    )
    ends_at = _normalize_datetime_for_compare(
        getattr(user, 'complimentary_access_ends_at', None)
    )

    if starts_at and current_dt < starts_at:
        return 'scheduled'
    if ends_at and current_dt > ends_at:
        return 'expired'
    return 'active'


def is_manual_access_window_active(user, now=None):
    """Return True if manual complimentary access is currently valid."""
    return get_manual_access_window_status(user, now=now) == 'active'


def has_global_complimentary_access(user):
    """
    Global complimentary access is enabled by the legacy boolean only when
    no explicit level restriction is configured.
    """
    if not user or not is_manual_access_window_active(user):
        return False
    level_ids = get_manual_access_level_ids(user)
    return bool(getattr(user, 'has_complimentary_access', False) and not level_ids)


def user_has_any_manual_access(user):
    """Return True when user has global or level-scoped manual access."""
    if not user or not is_manual_access_window_active(user):
        return False
    return has_global_complimentary_access(user) or bool(get_manual_access_level_ids(user))


def user_has_manual_access_for_level(user, niveau=None):
    """
    Return True if the user has complimentary access for a specific level.

    Rules:
    - If explicit complimentary levels exist, access is restricted to that set.
    - Otherwise, fallback to legacy global boolean.
    - If no level is provided, the user's current `niveau_pays` is used.
    """
    if not user or not is_manual_access_window_active(user):
        return False

    level_ids = get_manual_access_level_ids(user)
    if level_ids:
        target_level_id = _normalize_niveau_id(niveau)
        if target_level_id is None:
            target_level_id = _normalize_niveau_id(getattr(user, 'niveau_pays_id', None))
        return bool(target_level_id and target_level_id in level_ids)

    return bool(getattr(user, 'has_complimentary_access', False))


def _niveau_compatible(niveau_paye_id, niveau_id):
    """Un achat ouvre sa classe. Classe inconnue (ancien achat) ou demande sans
    classe précise : on ne bloque pas."""
    return niveau_id is None or niveau_paye_id is None or niveau_paye_id == niveau_id


def _abonnement_ouvre(user, niveau_id):
    abonnements = UserSubscription.objects.filter(user=user).only(
        'status', 'cancel_at_period_end', 'current_period_end', 'niveau_pays_id',
    )
    return any(a.is_active and _niveau_compatible(a.niveau_pays_id, niveau_id) for a in abonnements)


def _pass_ouvre(user, niveau_id):
    now = timezone.now()
    if niveau_id is None:
        return has_valid_active_pass(user, now=now)
    passes = list(AccessPass.objects.filter(user=user, ends_at__gt=now, is_revoked=False).order_by('-ends_at'))
    if not passes:
        return False
    # La classe d'un pass est celle de son paiement (le payeur peut être un parent).
    classes = dict(
        PaymentHistory.objects.filter(stripe_payment_intent_id__in=[p.stripe_payment_intent_id for p in passes])
        .values_list('stripe_payment_intent_id', 'niveau_pays_id')
    )
    candidats = [p for p in passes if _niveau_compatible(classes.get(p.stripe_payment_intent_id), niveau_id)]
    return bool(candidats) and bool(sync_refunded_passes(candidats[:3], max_stripe_checks=1))


def user_has_active_subscription_or_pass(user, niveau=None):
    """Return True if the user has premium access for the requested context."""
    if not user or not getattr(user, 'is_authenticated', False):
        return False

    # Allow staff/superusers by default
    if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
        return True

    # Cache results on user to avoid repeated queries within same request.
    # Cache key is contextualized by level id when available.
    resolved_level_id = _normalize_niveau_id(niveau)
    if resolved_level_id is None and niveau is None:
        resolved_level_id = _normalize_niveau_id(getattr(user, 'niveau_pays_id', None))
    cache_key = resolved_level_id if resolved_level_id is not None else '__any__'

    cached = getattr(user, '_has_subscription_access_cache', None)
    if isinstance(cached, bool) and cache_key == '__any__':
        return cached
    if not isinstance(cached, dict):
        cached = {}
    if cache_key in cached:
        return cached[cache_key]

    has_access = False
    if user_has_manual_access_for_level(user, niveau=niveau):
        has_access = True
    else:
        niveau_id = _normalize_niveau_id(niveau)
        has_access = _abonnement_ouvre(user, niveau_id) or _pass_ouvre(user, niveau_id)

    cached[cache_key] = has_access
    setattr(user, '_has_subscription_access_cache', cached)
    return has_access


def is_demo_content(user, content_type, content_obj):
    """Check if a content object is part of the user's niveau demo content.
    
    content_type: 'cours' | 'exercice'
    content_obj: the Cours or Exercice model instance
    """
    niveau = getattr(user, 'niveau_pays', None)
    if not niveau:
        return False

    if content_type == 'cours':
        notion_id = getattr(content_obj, 'notion_id', None)
        return notion_id and niveau.demo_notion_id == notion_id
    elif content_type == 'exercice':
        return niveau.demo_exercices.filter(pk=content_obj.pk).exists()
    return False


class HasActiveSubscriptionOrPass(BasePermission):
    """Allow access only to authenticated users with an active subscription or valid pass."""

    message = "Vous devez avoir un abonnement actif ou un pass en cours de validité pour accéder à ce contenu."

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return user_has_active_subscription_or_pass(user)
