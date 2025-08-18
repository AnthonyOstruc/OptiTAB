from django.contrib import admin
from .models import FicheSynthese


@admin.register(FicheSynthese)
class FicheSyntheseAdmin(admin.ModelAdmin):
    list_display = ['titre', 'notion', 'est_actif']
    list_filter = ['est_actif']
    search_fields = ['titre', 'notion__titre']
    ordering = ['notion']
    list_editable = ['est_actif']