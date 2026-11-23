"""Remet les abonnements d'accord avec Stripe (rattrape un webhook perdu).

    python manage.py synchroniser_stripe

Lancée automatiquement toutes les 6 heures en production (pass_expiration_scheduler).
"""
from django.core.management.base import BaseCommand

from subscriptions.synchronisation import synchroniser_abonnements


class Command(BaseCommand):
    help = "Remet les abonnements d'accord avec Stripe et ajoute les paiements manquants."

    def handle(self, *args, **options):
        bilan = synchroniser_abonnements()
        self.stdout.write(
            f"{bilan['verifies']} abonnement(s) vérifié(s), {bilan['corriges']} corrigé(s), "
            f"{bilan['paiements_ajoutes']} paiement(s) ajouté(s), {bilan['introuvables']} introuvable(s) "
            f"chez Stripe, {bilan['erreurs']} erreur(s)."
        )
