from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.services import StreakService


class Command(BaseCommand):
    help = 'Recompute and persist daily streaks for all active users (emits daily notifications).'

    def handle(self, *args, **options):
        User = get_user_model()
        count = 0
        for user in User.objects.filter(is_active=True):
            StreakService.refresh_user_streak(user, notify_on_increase=True)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Refreshed streaks for {count} users'))


