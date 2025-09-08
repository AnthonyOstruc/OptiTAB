from django.contrib import admin
from .models import Cours


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ['titre', 'chapitre', 'difficulty', 'est_actif']
    list_filter = ['difficulty', 'est_actif']
    search_fields = ['titre', 'chapitre__titre']
    ordering = ['chapitre']
    list_editable = ['est_actif']