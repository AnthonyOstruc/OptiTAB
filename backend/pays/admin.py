from django.contrib import admin
from .models import Pays, Niveau


class NiveauPaysInline(admin.TabularInline):
    """Inline pour gérer les niveaux associés à un pays"""
    model = Niveau
    extra = 1
    fields = ['nom', 'ordre', 'couleur', 'est_actif']


class PaysAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'code_iso', 'drapeau_emoji', 'est_actif', 'date_creation', 'date_modification']
    list_filter = ['est_actif', 'date_creation']
    search_fields = ['nom', 'code_iso']
    ordering = ['ordre', 'nom']
    readonly_fields = ['date_creation', 'date_modification']
    list_editable = ['est_actif']
    actions = ['activer_pays', 'desactiver_pays']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ['nom', 'code_iso', 'drapeau_emoji']
        }),
        ('Paramètres', {
            'fields': ['est_actif', 'ordre']
        }),
        ('Métadonnées', {
            'fields': ['date_creation', 'date_modification'],
            'classes': ['collapse']
        }),
    )
    
    inlines = [NiveauPaysInline]
    
    def activer_pays(self, request, queryset):
        """Action pour activer les pays sélectionnés"""
        updated = queryset.update(est_actif=True)
        self.message_user(request, f'{updated} pays activé(s) avec succès.')
    activer_pays.short_description = "Activer les pays sélectionnés"
    
    def desactiver_pays(self, request, queryset):
        """Action pour désactiver les pays sélectionnés"""
        updated = queryset.update(est_actif=False)
        self.message_user(request, f'{updated} pays désactivé(s) avec succès.')
    desactiver_pays.short_description = "Désactiver les pays sélectionnés"


class NiveauAdmin(admin.ModelAdmin):
    list_display = ['pays', 'nom', 'ordre', 'est_actif']
    list_filter = ['est_actif', 'pays']
    search_fields = ['pays__nom', 'nom']
    ordering = ['pays', 'ordre', 'nom']
    autocomplete_fields = ['pays']
    list_editable = ['ordre', 'est_actif']
    
    fieldsets = (
        ('Relation', {
            'fields': ['pays']
        }),
        ('Informations du niveau', {
            'fields': ['nom']
        }),
        ('Paramètres', {
            'fields': ['ordre', 'couleur', 'est_actif']
        }),
        ('Métadonnées', {
            'fields': ['date_creation', 'date_modification'],
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ['date_creation', 'date_modification']


# Enregistrement explicite des modèles
admin.site.register(Pays, PaysAdmin)
admin.site.register(Niveau, NiveauAdmin)