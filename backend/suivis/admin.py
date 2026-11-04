from django.contrib import admin
from .models import SuiviExercice, SuiviQuiz, QuizSubmission, ResultatQuizChapitre


@admin.register(SuiviExercice)
class SuiviExerciceAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercice', 'est_correct', 'points_obtenus', 'date_creation']
    list_filter = ['est_correct', 'exercice__notion']
    search_fields = ['user__email', 'exercice__titre']
    ordering = ['-date_creation']


@admin.register(SuiviQuiz)
class SuiviQuizAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_points', 'date_creation']
    list_filter = ['quiz__notion']
    search_fields = ['user__email', 'quiz__titre']
    ordering = ['-date_creation']


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'status', 'note', 'date_creation', 'date_correction']
    list_filter = ['status', 'quiz__notion', 'date_creation']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'quiz__titre']
    ordering = ['-date_creation']
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'quiz', 'status')
        }),
        ('Notation', {
            'fields': ('note', 'commentaire', 'corrige_par', 'date_correction')
        }),
        ('Notes administratives', {
            'fields': ('notes_admin',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ResultatQuizChapitre)
class ResultatQuizChapitreAdmin(admin.ModelAdmin):
    list_display = ['user', 'notion', 'note', 'bonnes', 'total', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['user__email', 'notion__titre']
    raw_id_fields = ['user', 'notion']
