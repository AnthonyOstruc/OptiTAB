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
            default=24,
            help='Limite de temps en heures pour chercher les passes expirés (défaut: 24h).',
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
        ).select_related(
            'user',
            'plan',
        )
        
        count = expired_passes.count()
        self.stdout.write(f"Passes expirés trouvés: {count}")
        
        if dry_run:
            for access_pass in expired_passes:
                self.stdout.write(
                    f"  - Pass #{access_pass.id}: {access_pass.user.email} "
                    f"({access_pass.plan.name}) expiré le {access_pass.ends_at}"
                )
            self.stdout.write(self.style.WARNING("Mode dry-run: aucun email envoyé."))
            return
        
        sent_count = 0
        error_count = 0
        
        for access_pass in expired_passes:
            try:
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
                    sent_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Email envoyé à {access_pass.user.email}")
                    )
                else:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f"✗ Échec envoi à {access_pass.user.email}")
                    )
                    
            except Exception as exc:
                error_count += 1
                logger.error(
                    "Erreur lors de l'envoi de l'email d'expiration pour le pass %s: %s",
                    access_pass.id,
                    exc,
                )
                self.stdout.write(
                    self.style.ERROR(f"✗ Erreur pour {access_pass.user.email}: {exc}")
                )
        
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Emails envoyés: {sent_count}"))
        if error_count:
            self.stdout.write(self.style.ERROR(f"Erreurs: {error_count}"))
