"""
Permission helpers for the Arena game.

Two layers:
1. Public visibility — `ArenaConfig.is_public`. Until True, only admins can play.
2. Premium gating — reuses subscriptions.permissions for paid features
   (advanced levels, full explanations, unlimited daily, etc.).
"""
from rest_framework.permissions import BasePermission

from subscriptions.permissions import user_has_active_subscription_or_pass

from .models import ArenaConfig


def is_admin(user):
    return bool(
        user
        and getattr(user, 'is_authenticated', False)
        and (getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False))
    )


def is_premium(user):
    """Subscription, pass or complimentary access."""
    return user_has_active_subscription_or_pass(user)


def game_is_visible_to(user):
    """Public visibility check."""
    config = ArenaConfig.get_solo()
    if config.is_public:
        return True
    return is_admin(user)


class ArenaVisible(BasePermission):
    """Block access entirely while game is in private/admin-only mode."""

    message = "Le jeu Arena n'est pas encore disponible publiquement."

    def has_permission(self, request, view):
        return game_is_visible_to(getattr(request, 'user', None))


class ArenaAdminOnly(BasePermission):
    message = "Réservé à l'administration."

    def has_permission(self, request, view):
        return is_admin(getattr(request, 'user', None))
