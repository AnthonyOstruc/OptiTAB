from django.contrib import admin
from .models import SynthesisSheet


@admin.register(SynthesisSheet)
class SynthesisSheetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'notion', 'get_matiere', 'difficulty', 'reading_time_minutes', 'est_actif', 'date_creation')
    list_filter = ('difficulty', 'est_actif', 'notion__theme__matiere', 'date_creation')
    search_fields = ('titre', 'notion__titre', 'summary')
    ordering = ('notion', 'ordre', 'titre')
    
    fieldsets = (
        (None, {
            'fields': ('titre', 'notion', 'ordre', 'difficulty', 'est_actif')
        }),
        ('Contenu', {
            'fields': ('summary', 'reading_time_minutes'),
            'classes': ('wide',)
        }),
        ('Données structurées', {
            'fields': ('key_points', 'formulas', 'examples'),
            'classes': ('collapse',)
        }),
    )
    
    def get_matiere(self, obj):
        return obj.notion.theme.matiere.titre if obj.notion and obj.notion.theme and obj.notion.theme.matiere else '-'
    get_matiere.short_description = 'Matière'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'notion', 
            'notion__theme',
            'notion__theme__matiere'
        )
