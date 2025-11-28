"""
Administration pour les exercices - Interface admin Django
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from core.admin import ContentModelAdmin, BaseModelAdmin
from .models import Matiere, Theme, Notion, Exercice, MatiereContexte, ExerciceImage
from .services import duplicate_theme_deep


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    """Administration des matières"""
    list_display = ['titre', 'ordre', 'est_actif', 'show_on_home']
    list_filter = ['est_actif', 'show_on_home']
    search_fields = ['titre', 'description']
    list_editable = ['ordre']
    ordering = ['ordre', 'titre']
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('titre', 'description')
        }),
        # Associations supprimées: gérées via MatiereContexte
        (_('Configuration'), {
            'fields': ('ordre', 'svg_icon', 'est_actif', 'show_on_home'),
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
    
    # Template personnalisé pour ajouter un formulaire de duplication sur la page de modification
    change_form_template = 'admin/curriculum/theme/change_form.html'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('matiere', 'contexte', 'contexte__niveau', 'contexte__niveau__pays')

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['duplicate_contextes'] = (
            MatiereContexte.objects.select_related('matiere', 'niveau', 'niveau__pays')
            .all()
            .order_by('matiere__ordre', 'niveau__pays__nom', 'niveau__ordre')
        )
        return super().changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        # Assurer l'alignement: matiere = contexte.matiere
        if getattr(obj, 'contexte', None) and getattr(obj.contexte, 'matiere_id', None):
            if obj.matiere_id != obj.contexte.matiere_id:
                obj.matiere_id = obj.contexte.matiere_id
        super().save_model(request, obj, form, change)

    # Actions d'objet personnalisées: ajouter un bouton "Dupliquer" sur la page de modification
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/duplicate/',
                self.admin_site.admin_view(self.process_duplicate),
                name='curriculum_theme_duplicate',
            ),
        ]
        return custom_urls + urls

    def process_duplicate(self, request, object_id):
        theme = self.get_object(request, object_id)
        if theme is None:
            messages.error(request, "Thème introuvable")
            return redirect('admin:curriculum_theme_changelist')

        if request.method == 'GET':
            # Page dédiée avec un vrai formulaire pour éviter tout conflit avec le change form
            from django.template.response import TemplateResponse
            context = {
                **self.admin_site.each_context(request),
                'original': theme,
                'title': _('Dupliquer le thème'),
                'opts': self.model._meta,
                'duplicate_contextes': MatiereContexte.objects.select_related('matiere', 'niveau', 'niveau__pays')
                    .all().order_by('matiere__ordre', 'niveau__pays__nom', 'niveau__ordre'),
                'media': self.media,
                'has_view_permission': self.has_view_permission(request, theme),
            }
            return TemplateResponse(request, 'admin/curriculum/theme/duplicate_form.html', context)

        # POST: créer la copie
        contexte_id = request.POST.get('contexte')
        titre = (request.POST.get('titre') or '').strip()
        if not contexte_id:
            messages.error(request, "Veuillez sélectionner un contexte cible")
            return redirect(request.path)
        try:
            target_contexte = MatiereContexte.objects.get(pk=contexte_id)
        except MatiereContexte.DoesNotExist:
            messages.error(request, "Contexte cible introuvable")
            return redirect(request.path)

        try:
            new_theme = duplicate_theme_deep(theme, target_contexte, titre or None)
            messages.success(request, format_html(
                "Copie créée: <a href=\"{}\"><strong>{}</strong></a>",
                request.build_absolute_uri(f"/admin/curriculum/theme/{new_theme.pk}/change/"),
                new_theme.titre
            ))
            return redirect('admin:curriculum_theme_change', theme.pk)
        except Exception as e:
            messages.error(request, f"Erreur lors de la duplication: {e}")
            return redirect(request.path)


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


@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    """
    Administration des exercices
    """
    list_display = [
        'titre', 'notion_info', 'difficulty_display',
        'access_scope', 'status_display', 'date_creation'
    ]
    list_filter = [
        'notion__theme__matiere',
        'notion__theme',
        'notion',
        'difficulty',
        'access_scope',
        'est_actif',
        'date_creation'
    ]
    search_fields = [
        'titre', 'contenu', 'question', 'reponse_correcte', 'exercice_type',
        'notion__titre',
        'notion__theme__titre', 'notion__theme__matiere__titre'
    ]
    list_editable = ['access_scope']
    ordering = ['notion', 'ordre', 'titre']
    
    # Inline pour gérer les images d'exercice
    class ExerciceImageInline(admin.TabularInline):
        model = ExerciceImage
        extra = 1
        fields = ("preview", "image", "image_type", "position", "legende")
        readonly_fields = ("preview",)
        can_delete = True

        def preview(self, obj):
            if getattr(obj, "image", None):
                try:
                    return format_html('<img src="{}" style="height: 80px; max-width: 140px; object-fit: cover;" />', obj.image.url)
                except Exception:
                    return "(aperçu indisponible)"
            return "-"

        preview.short_description = _("Aperçu")
    
    inlines = [ExerciceImageInline]
    
    # Utiliser fieldsets au lieu de fields
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('titre', 'notion')  # ✅ notion est obligatoire
        }),
        (_('Contenu de l\'exercice'), {
            'fields': ('contenu', 'question', 'reponse_correcte'),
        }),
        (_('Configuration'), {
            'fields': ('difficulty', 'access_scope'),
            'classes': ['collapse']
        }),
        (_('Statut et métadonnées'), {
            'fields': ('est_actif', 'date_creation', 'date_modification'),
            'classes': ['collapse']
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')
    
    def notion_info(self, obj):
        """Affiche les informations de la notion"""
        return format_html(
            '<strong>{}</strong><br><small>{} | {}</small>',
            obj.notion.titre,
            obj.notion.theme.titre,
            obj.notion.theme.matiere.titre
        )
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
        return super().get_queryset(request).select_related(
            'notion', 'notion__theme',
            'notion__theme__matiere'
        )


# Administration dédiée aux images d'exercice
@admin.register(ExerciceImage)
class ExerciceImageAdmin(admin.ModelAdmin):
    list_display = ("id", "exercice", "image_type", "position", "legende", "image_link")
    list_filter = ("image_type",)
    search_fields = ("exercice__titre", "legende")
    ordering = ("exercice", "position", "id")

    def image_link(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html('<a href="{}" target="_blank">Voir</a>', obj.image.url)
            except Exception:
                return "(lien indisponible)"
        return "-"

    image_link.short_description = _("Image")

# Configuration des titres de l'interface admin
admin.site.site_header = "Administration OptiTAB - Exercices"
admin.site.site_title = "OptiTAB Admin"
admin.site.index_title = "Gestion des exercices et contenus pédagogiques"
