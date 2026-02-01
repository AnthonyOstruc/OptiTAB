from __future__ import annotations

from typing import Optional

from subscriptions.models import UserSubscription


def _get_locked_subscription_level(user) -> Optional['Niveau']:
    """
    Retourne le niveau verrouillé par l'abonnement actif de l'utilisateur, le cas échéant.
    """
    if not user or not getattr(user, 'id', None):
        return None
    try:
        subscription = user.subscription
    except UserSubscription.DoesNotExist:
        return None
    if not subscription.niveau_pays_id:
        return None
    # Considérer le verrou actif tant que l'accès n'est pas totalement terminé
    if subscription.status == 'canceled' and not subscription.is_active:
        return None
    return subscription.niveau_pays


def _lock_message(niveau) -> str:
    if not niveau:
        return "Votre abonnement ne permet pas de changer de niveau pour le moment."
    pays_nom = getattr(niveau.pays, 'nom', '').strip()
    if pays_nom:
        return (
            f"Votre abonnement est limité au niveau {niveau.nom} ({pays_nom}). "
            "Contactez le support pour changer de niveau."
        )
    return (
        f"Votre abonnement est limité au niveau {niveau.nom}. "
        "Contactez le support pour changer de niveau."
    )


def validate_subscription_level_change(
    user,
    *,
    niveau_id: Optional[int] = None,
    pays_id: Optional[int] = None,
    niveau_field_present: bool = False,
    pays_field_present: bool = False
) -> Optional[str]:
    """
    Anciennement: validation pour empêcher de quitter un niveau verrouillé.
    Désormais, on autorise l'utilisateur à modifier librement sa configuration,
    même sans abonnement actif pour ce niveau. Les restrictions d'accès sont
    appliquées côté contenu (chapitres verrouillés) plutôt qu'au niveau de la
    configuration.
    """
    return None
