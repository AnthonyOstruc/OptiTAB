"""Vérification régulière auprès de Stripe : le filet de sécurité des webhooks.

Un webhook peut se perdre (serveur indisponible, erreur passagère...). Cette
vérification remet chaque abonnement en cours d'accord avec Stripe (statut,
dates, résiliation) et enregistre les paiements qui manquent dans l'historique.
Elle passe par les mêmes traitements que les webhooks : une seule logique.

Lancée toutes les 6 heures par la tâche de fond (pass_expiration_scheduler) en
production, ou à la main : `python manage.py synchroniser_stripe`.
"""
import logging
from datetime import timedelta

from django.utils import timezone

from .handlers import (
    _create_invoice_payment_history,
    handle_payment_succeeded,
    handle_subscription_deleted,
    handle_subscription_updated,
)
from .helpers import _from_timestamp
from .models import PaymentHistory, UserSubscription
from .stripe_client import stripe, stripe_error

logger = logging.getLogger(__name__)

# Au-delà, un changement rattrapé est enregistré sans courriel au client
# (pas de reçu ni de « résiliation » envoyés des semaines plus tard).
DELAI_COURRIEL = timedelta(days=3)


def _recent(horodatage, maintenant):
    moment = _from_timestamp(horodatage)
    return moment is None or maintenant - moment <= DELAI_COURRIEL


def _synchroniser_paiements(local, distant, maintenant):
    """Enregistre les factures payées absentes de l'historique. Renvoie leur nombre."""
    ajoutes = 0
    factures = stripe.Invoice.list(subscription=local.stripe_subscription_id, status='paid', limit=100)
    for facture in factures.auto_paging_iter():
        if PaymentHistory.objects.filter(stripe_invoice_id=facture.get('id')).exists():
            continue
        if _recent(facture.get('created'), maintenant):
            handle_payment_succeeded(facture)
        else:
            metadonnees = {**(distant.get('metadata') or {}), **(facture.get('metadata') or {})}
            paiement, cree = _create_invoice_payment_history(local, facture, facture.get('id'), metadonnees)
            if paiement and cree:
                paiement.email_sent = True
                paiement.save(update_fields=['email_sent'])
        ajoutes += 1
    return ajoutes


def synchroniser_abonnements(maintenant=None):
    """Remet les abonnements en cours d'accord avec Stripe. Idempotent.

    Un abonnement introuvable chez Stripe n'est jamais modifié : il peut venir de
    l'autre mode (essai fait en test et enregistré dans la base réelle).
    """
    maintenant = maintenant or timezone.now()
    bilan = {'verifies': 0, 'corriges': 0, 'paiements_ajoutes': 0, 'introuvables': 0, 'erreurs': 0}
    abonnements = (
        UserSubscription.objects.exclude(status='canceled')
        .exclude(stripe_subscription_id__isnull=True).exclude(stripe_subscription_id='')
    )
    for local in abonnements:
        bilan['verifies'] += 1
        try:
            distant = stripe.Subscription.retrieve(local.stripe_subscription_id)
        except stripe_error.InvalidRequestError:
            bilan['introuvables'] += 1
            continue
        try:
            avant = (local.status, local.current_period_end, local.cancel_at_period_end)
            notifier = _recent(distant.get('canceled_at'), maintenant)
            if distant.get('status') == 'canceled':
                handle_subscription_deleted(distant, notifier=notifier)
            else:
                handle_subscription_updated(distant, notifier=notifier)
            local.refresh_from_db()
            if (local.status, local.current_period_end, local.cancel_at_period_end) != avant:
                bilan['corriges'] += 1
            bilan['paiements_ajoutes'] += _synchroniser_paiements(local, distant, maintenant)
        except Exception:
            bilan['erreurs'] += 1
            logger.exception("Synchronisation Stripe : échec pour l'abonnement %s", local.stripe_subscription_id)
    logger.info("Synchronisation Stripe : %s", bilan)
    return bilan
