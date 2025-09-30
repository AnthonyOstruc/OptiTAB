from django.contrib import admin
from .models import Quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['titre', 'notion', 'difficulty', 'duree_minutes', 'est_actif']
    list_filter = ['difficulty', 'est_actif']
    search_fields = ['titre', 'notion__titre']
    ordering = ['notion', 'ordre']
    list_editable = ['est_actif']