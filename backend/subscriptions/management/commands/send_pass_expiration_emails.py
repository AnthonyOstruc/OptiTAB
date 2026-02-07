"""
Management command pour envoyer des emails de notification d'expiration de pass.
À exécuter périodiquement via cron (ex: toutes les heures).

Usage:
    python manage.py send_pass_expiration_emails
"""
import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from subscriptions.models import AccessPass, PaymentHistory
from core.services import EmailService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Envoie des emails de notification aux utilisateurs dont le pass a expiré."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les passes expirés sans envoyer les emails.',
        )
        parser.add_argument(
            '--hours-ago',
            type=int,
            default=72,
            help='Limite de temps en heures pour chercher les passes expirés (défaut: 72h).',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        hours_ago = options['hours_ago']
        
        now = timezone.now()
        cutoff_time = now - timedelta(hours=hours_ago)

        # Trouver les passes expirés récemment qui n'ont pas encore reçu d'email
        expired_passes = AccessPass.objects.filter(
            ends_at__lte=now,
            ends_at__gte=cutoff_time,
            expiration_email_sent=False,
            is_revoked=False,
        ).select_related(
            'user',
            'plan',
        )
        
        if dry_run:
            for access_pass in expired_passes:
                self.stdout.write(
                    f"  - Pass #{access_pass.id}: {access_pass.user.email} "
                    f"({access_pass.plan.name}) expiré le {access_pass.ends_at}"
                )
            self.stdout.write(self.style.WARNING("Mode dry-run: aucun email envoyé."))
            return
        
        for access_pass in expired_passes:
            try:
                user = access_pass.user

                # Ne pas spammer: si l'utilisateur a encore accès (admin/staff, accès manuel,
                # abonnement actif ou autre pass actif), on ne send pas mais on marque le pass
                # comme "traité" afin d'assurer l'idempotence.
                if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
                    with transaction.atomic():
                        AccessPass.objects.filter(pk=access_pass.pk).update(
                            expiration_email_sent=True
                        )
                    continue

                still_has_access = False
                if getattr(user, 'has_complimentary_access', False):
                    still_has_access = True
                else:
                    try:
                        subscription = user.subscription
                    except Exception:
                        subscription = None
                    if subscription and getattr(subscription, 'is_active', False):
                        still_has_access = True
                    else:
                        other_active_pass = AccessPass.objects.filter(
                            user=user,
                            ends_at__gt=now,
                            is_revoked=False,
                        ).exists()
                        if other_active_pass:
                            still_has_access = True

                if still_has_access:
                    with transaction.atomic():
                        AccessPass.objects.filter(pk=access_pass.pk).update(
                            expiration_email_sent=True
                        )
                    continue

                # Récupérer le niveau depuis PaymentHistory si disponible
                niveau = None
                payment_history = PaymentHistory.objects.filter(
                    stripe_payment_intent_id=access_pass.stripe_payment_intent_id
                ).select_related('niveau_pays', 'niveau_pays__pays').first()
                
                if payment_history:
                    niveau = payment_history.niveau_pays
                
                # Envoyer l'email
                success = EmailService.send_pass_expiration_notification(
                    user=access_pass.user,
                    access_pass=access_pass,
                    niveau=niveau,
                )
                
                if success:
                    # Marquer l'email comme envoyé
                    with transaction.atomic():
                        AccessPass.objects.filter(pk=access_pass.pk).update(
                            expiration_email_sent=True
                        )

                    # Notifier aussi l'admin (suivi)
                    try:
                        EmailService.send_pass_expiration_notification_to_admin(
                            user=access_pass.user,
                            access_pass=access_pass,
                            niveau=niveau,
                        )
                    except Exception:
                        # La méthode gère déjà ses propres logs; ne pas faire échouer le job.
                        pass
                    
            except Exception as exc:
                logger.error(
                    "Erreur lors de l'envoi de l'email d'expiration pour le pass %s: %s",
                    access_pass.id,
                    exc,
                )
