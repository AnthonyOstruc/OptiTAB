from django.utils import timezone
from rest_framework.permissions import BasePermission

from .models import AccessPass, UserSubscription


def user_has_active_subscription_or_pass(user):
    """Return True if the user has an active subscription or non-expired pass."""
    if not user or not getattr(user, 'is_authenticated', False):
        return False

    # Allow staff/superusers by default
    if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
        return True
    if getattr(user, 'has_complimentary_access', False):
        return True

    # Cache result on user to avoid repeated queries within same request
    cached = getattr(user, '_has_subscription_access_cache', None)
    if cached is not None:
        return cached

    has_access = False

    try:
        subscription = user.subscription
    except (UserSubscription.DoesNotExist, AttributeError):  # pragma: no cover - handled by except
        subscription = None
    except Exception:  # pragma: no cover - defensive
        subscription = None

    if subscription and subscription.is_active:
        has_access = True
    else:
        now = timezone.now()
        has_access = AccessPass.objects.filter(user=user, ends_at__gt=now).exists()

    setattr(user, '_has_subscription_access_cache', has_access)
    return has_access


class HasActiveSubscriptionOrPass(BasePermission):
    """Allow access only to authenticated users with an active subscription or valid pass."""

    message = "Vous devez avoir un abonnement actif ou un pass en cours de validité pour accéder à ce contenu."

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        return user_has_active_subscription_or_pass(user)
