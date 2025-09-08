from django.contrib import admin
from .models import SuiviExercice, SuiviQuiz


@admin.register(SuiviExercice)
class SuiviExerciceAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercice', 'est_correct', 'points_obtenus', 'date_creation']
    list_filter = ['est_correct', 'exercice__chapitre']
    search_fields = ['user__email', 'exercice__titre']
    ordering = ['-date_creation']


@admin.register(SuiviQuiz)
class SuiviQuizAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_points', 'date_creation']
    list_filter = ['quiz__chapitre']
    search_fields = ['user__email', 'quiz__titre']
    ordering = ['-date_creation']