from django.core.management.base import BaseCommand
from django.db import transaction

from curriculum.models import Notion, Exercice
from cours.models import Cours
from quiz.models import Quiz


class Command(BaseCommand):
    help = 'Purge toutes les donnees Notion, Exercice, Cours et Quiz (irreversible)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirme la purge complète des données',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write('Vous devez confirmer avec --confirm pour lancer la purge.')
            return

        quiz_count = Quiz.objects.count()
        cours_count = Cours.objects.count()
        exercice_count = Exercice.objects.count()
        notion_count = Notion.objects.count()

        self.stdout.write(
            'Purge en cours... Quiz: %d, Cours: %d, Exercices: %d, Notions: %d'
            % (quiz_count, cours_count, exercice_count, notion_count)
        )

        # Supprimer dans un ordre sûr; la suppression des notions cascade aussi
        deleted_quiz, _ = Quiz.objects.all().delete()
        deleted_cours, _ = Cours.objects.all().delete()
        deleted_exercices, _ = Exercice.objects.all().delete()
        deleted_notions, _ = Notion.objects.all().delete()

        self.stdout.write(
            'Purge terminee. Quiz supprimes: %d, Cours supprimes: %d, '
            'Exercices supprimes: %d, Notions supprimees: %d'
            % (deleted_quiz, deleted_cours, deleted_exercices, deleted_notions)
        )


