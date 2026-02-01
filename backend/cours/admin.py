from django.contrib import admin
from django.utils.html import format_html
from .models import Cours, CoursImage


class CoursImageInline(admin.TabularInline):
    model = CoursImage
    extra = 0
    fields = ("preview", "image", "image_type", "position", "legende")
    readonly_fields = ("preview",)
    can_delete = True

    def preview(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html('<img src="{}" style="height: 80px; max-width: 140px; object-fit: cover;" />', obj.image.url)
            except Exception:
                # En cas d'image manquante (fichier supprimé), on évite de casser l'admin
                return "(aperçu indisponible)"
        return "-"

    preview.short_description = "Aperçu"


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ['titre', 'notion', 'access_scope', 'est_actif', 'pdf_link']
    list_filter = ['access_scope', 'est_actif']
    search_fields = ['titre', 'notion__titre']
    ordering = ['notion']
    list_editable = ['est_actif', 'access_scope']
    fields = (
        'notion',
        'titre',
        'contenu',
        'access_scope',
        'video_url',
        'pdf_file',
        'est_actif',
        'date_creation',
        'date_modification'
    )
    readonly_fields = ('date_creation', 'date_modification')
    inlines = [CoursImageInline]
    
    def get_form(self, request, obj=None, **kwargs):
        """Personnaliser le formulaire pour nettoyer l'affichage du contenu"""
        form = super().get_form(request, obj, **kwargs)
        
        # Personnaliser le widget du champ contenu pour un meilleur affichage
        if 'contenu' in form.base_fields:
            from django.forms import Textarea
            form.base_fields['contenu'].widget = Textarea(attrs={
                'rows': 15,
                'cols': 80,
                'style': 'white-space: pre-wrap; font-family: monospace;'
            })
        
        return form
    
    def save_model(self, request, obj, form, change):
        """Nettoyer le contenu avant sauvegarde pour supprimer les lignes vides multiples"""
        if obj.contenu:
            # Supprimer les lignes vides multiples et les espaces en fin de ligne
            lines = obj.contenu.split('\n')
            cleaned_lines = []
            prev_empty = False
            
            for line in lines:
                stripped_line = line.rstrip()
                if stripped_line:  # Ligne non vide
                    cleaned_lines.append(stripped_line)
                    prev_empty = False
                elif not prev_empty:  # Première ligne vide consécutive
                    cleaned_lines.append('')
                    prev_empty = True
                # Ignorer les lignes vides supplémentaires
            
            obj.contenu = '\n'.join(cleaned_lines)
        
        super().save_model(request, obj, form, change)

    def pdf_link(self, obj):
        pdf = getattr(obj, 'pdf_file', None)
        if pdf:
            try:
                return format_html('<a href="{}" target="_blank">Télécharger</a>', pdf.url)
            except Exception:
                return '(lien indisponible)'
        return '-'

    pdf_link.short_description = 'PDF'


@admin.register(CoursImage)
class CoursImageAdmin(admin.ModelAdmin):
    list_display = ("id", "cours", "image_type", "position", "legende", "image_link")
    list_filter = ("image_type",)
    search_fields = ("cours__notion__titre", "legende")
    ordering = ("cours", "position", "id")

    def image_link(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html('<a href="{}" target="_blank">Voir</a>', obj.image.url)
            except Exception:
                return "(lien indisponible)"
        return "-"

    image_link.short_description = "Image"
