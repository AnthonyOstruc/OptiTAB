from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Remet tous les XP et niveaux des utilisateurs à zéro'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirme la remise à zéro (obligatoire)',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR(
                    'Vous devez confirmer avec --confirm pour remettre les XP à zéro'
                )
            )
            return

        users_count = User.objects.all().count()
        
        self.stdout.write(
            f'Remise à zéro des XP et niveaux pour {users_count} utilisateur(s)...'
        )
        
        # Remettre XP et niveau à 0 pour tous les utilisateurs
        updated = User.objects.all().update(xp=0, level=0)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ {updated} utilisateur(s) mis à jour avec succès.\n'
                f'📊 Tous les XP et niveaux ont été remis à zéro.\n'
                f'🎮 Seuls les quiz donnent maintenant des XP.'
            )
        )
