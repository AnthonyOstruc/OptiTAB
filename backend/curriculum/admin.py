"""
Administration pour les exercices - Interface admin Django
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from core.admin import ContentModelAdmin, BaseModelAdmin
from .models import Matiere, Theme, Notion, Chapitre, Exercice, MatiereContexte


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    """Administration des matières"""
    list_display = ['titre', 'ordre', 'est_actif']
    list_filter = ['est_actif']
    search_fields = ['titre', 'description']
    list_editable = ['ordre']
    ordering = ['ordre', 'titre']
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('titre', 'description')
        }),
        # Associations supprimées: gérées via MatiereContexte
        (_('Configuration'), {
            'fields': ('ordre', 'svg_icon', 'est_actif'),
            'classes': ['collapse']
        }),
    )
    
    # Compteurs/associations supprimés


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """
    Administration des thèmes
    """
    list_display = ['titre', 'matiere_info', 'contexte_info', 'ordre', 'status_display', 'date_creation']
    list_filter = ['matiere', 'contexte__niveau__pays', 'contexte__niveau', 'est_actif', 'date_creation']
    search_fields = ['titre', 'matiere__titre']
    list_editable = ['ordre']
    ordering = ['matiere', 'ordre', 'titre']
    
    # Utiliser fieldsets au lieu de fields
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('titre', 'matiere', 'contexte')  # ✅ rattacher le thème à un contexte
        }),
        (_('Configuration'), {
            'fields': ('ordre', 'couleur', 'svg_icon'),
            'classes': ['collapse']
        }),
        (_('Statut et métadonnées'), {
            'fields': ('est_actif', 'date_creation', 'date_modification'),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')
    
    def matiere_info(self, obj):
        return format_html('<strong>{}</strong>', obj.matiere.titre)

    def contexte_info(self, obj):
        c = getattr(obj, 'contexte', None)
        if not c:
            return '-'
        p = getattr(c.niveau, 'pays', None)
        pays_nom = p.nom if p else ''
        return format_html('<small>{} - {}</small>', pays_nom, c.niveau.nom)
    contexte_info.short_description = _('Contexte')
    matiere_info.short_description = _('Matière')
    
    def status_display(self, obj):
        """Affiche le statut avec indicateur visuel"""
        if obj.est_actif:
            return format_html('<span style="color: green;">●</span> Actif')
        else:
            return format_html('<span style="color: red;">●</span> Inactif')
    status_display.short_description = _('Statut')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('matiere', 'contexte', 'contexte__niveau', 'contexte__niveau__pays')


@admin.register(MatiereContexte)
class MatiereContexteAdmin(admin.ModelAdmin):
    """Administration des contextes Matière + Niveau"""
    list_display = ['matiere', 'niveau', 'pays_display', 'ordre', 'est_actif']
    list_filter = ['matiere', 'niveau__pays', 'niveau', 'est_actif']
    search_fields = ['matiere__titre', 'niveau__nom', 'niveau__pays__nom']
    ordering = ['matiere__ordre', 'niveau__pays__nom', 'niveau__ordre']

    fieldsets = (
        (_('Informations de base'), {
            'fields': ('matiere', 'niveau', 'titre', 'description')
        }),
        (_('Configuration'), {
            'fields': ('ordre', 'couleur', 'svg_icon', 'est_actif'),
            'classes': ['collapse']
        }),
        (_('Métadonnées'), {
            'fields': ('date_creation', 'date_modification'),
            'classes': ['collapse']
        }),
    )

    readonly_fields = ('date_creation', 'date_modification')

    def pays_display(self, obj):
        p = getattr(obj.niveau, 'pays', None)
        return p.nom if p else '-'
    pays_display.short_description = _('Pays')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('matiere', 'niveau', 'niveau__pays')


@admin.register(Notion)
class NotionAdmin(admin.ModelAdmin):
    """
    Administration des notions
    """
    list_display = ['titre', 'theme_info', 'ordre', 'status_display', 'date_creation']
    list_filter = ['theme__matiere', 'theme', 'est_actif', 'date_creation']
    search_fields = ['titre', 'theme__titre', 'theme__matiere__titre']
    list_editable = ['ordre']
    ordering = ['theme', 'ordre', 'titre']
    
    # Utiliser fieldsets au lieu de fields
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('titre', 'theme')  # ✅ theme est obligatoire
        }),
        (_('Configuration'), {
            'fields': ('ordre', 'couleur', 'svg_icon'),
            'classes': ['collapse']
        }),
        (_('Statut et métadonnées'), {
            'fields': ('est_actif', 'date_creation', 'date_modification'),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')
    
    def theme_info(self, obj):
        return format_html('<strong>{}</strong><br><small>{}</small>', obj.theme.titre, obj.theme.matiere.titre)
    theme_info.short_description = _('Thème')
    
    def status_display(self, obj):
        """Affiche le statut avec indicateur visuel"""
        if obj.est_actif:
            return format_html('<span style="color: green;">●</span> Actif')
        else:
            return format_html('<span style="color: red;">●</span> Inactif')
    status_display.short_description = _('Statut')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('theme', 'theme__matiere')


@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    """
    Administration des chapitres
    """
    list_display = ['titre', 'notion_info', 'difficulty_display', 'ordre', 'status_display', 'date_creation']
    list_filter = ['notion__theme__matiere', 'notion__theme', 'notion', 'difficulty', 'est_actif', 'date_creation']
    search_fields = [
        'titre', 'contenu',
        'notion__titre', 'notion__theme__titre', 'notion__theme__matiere__titre'
    ]
    list_editable = ['ordre']
    ordering = ['notion', 'ordre', 'titre']
    
    # Utiliser fieldsets au lieu de fields
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('titre', 'notion')  # ✅ notion est obligatoire
        }),
        (_('Contenu'), {
            'fields': ('contenu',),
        }),
        (_('Configuration'), {
            'fields': ('ordre', 'difficulty'),
            'classes': ['collapse']
        }),
        (_('Statut et métadonnées'), {
            'fields': ('est_actif', 'date_creation', 'date_modification'),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')
    
    def notion_info(self, obj):
        return format_html('<strong>{}</strong><br><small>{} | {}</small>', obj.notion.titre, obj.notion.theme.titre, obj.notion.theme.matiere.titre)
    notion_info.short_description = _('Notion')
    
    def difficulty_display(self, obj):
        """Affiche la difficulté avec couleur"""
        colors = {
            'facile': 'green',
            'moyen': 'orange',
            'difficile': 'red'
        }
        color = colors.get(obj.difficulty, 'gray')
        return format_html(
            '<span style="color: {};">● {}</span>',
            color,
            obj.get_difficulty_display()
        )
    difficulty_display.short_description = _('Difficulté')
    
    def status_display(self, obj):
        """Affiche le statut avec indicateur visuel"""
        if obj.est_actif:
            return format_html('<span style="color: green;">●</span> Actif')
        else:
            return format_html('<span style="color: red;">●</span> Inactif')
    status_display.short_description = _('Statut')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('notion', 'notion__theme', 'notion__theme__matiere')


@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    """
    Administration des exercices
    """
    list_display = [
        'titre', 'chapitre_info', 'points', 'difficulty_display', 
        'ordre', 'status_display', 'date_creation'
    ]
    list_filter = [
        'chapitre__notion__theme__matiere',
        'chapitre__notion__theme',
        'chapitre__notion',
        'chapitre',
        'difficulty',
        'points',
        'est_actif',
        'date_creation'
    ]
    search_fields = [
        'titre', 'contenu', 'question', 'reponse_correcte',
        'chapitre__titre', 'chapitre__notion__titre',
        'chapitre__notion__theme__titre', 'chapitre__notion__theme__matiere__titre'
    ]
    list_editable = ['ordre', 'points']
    ordering = ['chapitre', 'ordre', 'titre']
    
    # Utiliser fieldsets au lieu de fields
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('titre', 'chapitre')  # ✅ chapitre est obligatoire
        }),
        (_('Contenu de l\'exercice'), {
            'fields': ('contenu', 'question', 'reponse_correcte'),
        }),
        (_('Configuration'), {
            'fields': ('ordre', 'difficulty', 'points'),
            'classes': ['collapse']
        }),
        (_('Statut et métadonnées'), {
            'fields': ('est_actif', 'date_creation', 'date_modification'),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')
    
    def chapitre_info(self, obj):
        """Affiche les informations du chapitre"""
        return format_html(
            '<strong>{}</strong><br><small>{} | {} | {}</small>',
            obj.chapitre.titre,
            obj.chapitre.notion.titre,
            obj.chapitre.notion.theme.titre,
            obj.chapitre.notion.theme.matiere.titre
        )
    chapitre_info.short_description = _('Chapitre')
    
    def difficulty_display(self, obj):
        """Affiche la difficulté avec couleur"""
        colors = {
            'facile': 'green',
            'moyen': 'orange',
            'difficile': 'red'
        }
        color = colors.get(obj.difficulty, 'gray')
        return format_html(
            '<span style="color: {};">● {}</span>',
            color,
            obj.get_difficulty_display()
        )
    difficulty_display.short_description = _('Difficulté')
    
    def status_display(self, obj):
        """Affiche le statut avec indicateur visuel"""
        if obj.est_actif:
            return format_html('<span style="color: green;">●</span> Actif')
        else:
            return format_html('<span style="color: red;">●</span> Inactif')
    status_display.short_description = _('Statut')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'chapitre', 'chapitre__notion', 'chapitre__notion__theme',
            'chapitre__notion__theme__matiere'
        )


# Configuration des titres de l'interface admin
admin.site.site_header = "Administration OptiTAB - Exercices"
admin.site.site_title = "OptiTAB Admin"
admin.site.index_title = "Gestion des exercices et contenus pédagogiques"
