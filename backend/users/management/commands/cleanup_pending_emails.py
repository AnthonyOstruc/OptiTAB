from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser


class Command(BaseCommand):
    help = "Nettoie les demandes de changement d'email expirées (24h)."

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=24)
        expired_qs = CustomUser.objects.filter(
            pending_email__isnull=False,
            pending_email_sent_at__lt=cutoff,
        )
        count = expired_qs.update(
            pending_email=None,
            pending_email_token=None,
            pending_email_sent_at=None,
        )
        self.stdout.write(self.style.SUCCESS(f"{count} entrées nettoyées."))
