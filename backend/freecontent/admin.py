from django.contrib import admin

from .models import FreeLearningResource


@admin.register(FreeLearningResource)
class FreeLearningResourceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'resource_type', 'matiere', 'niveau', 'est_publie', 'est_actif', 'ordre')
    list_filter = ('resource_type', 'est_publie', 'est_actif', 'matiere', 'niveau')
    search_fields = ('titre', 'accroche', 'excerpt')
    list_editable = ('ordre', 'est_publie', 'est_actif')
    prepopulated_fields = {'slug': ('titre',)}
    autocomplete_fields = ('matiere', 'niveau', 'notion')
    ordering = ('resource_type', 'ordre')


# Register your models here.
