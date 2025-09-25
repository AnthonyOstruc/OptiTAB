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
    list_display = ['titre', 'chapitre', 'difficulty', 'est_actif']
    list_filter = ['difficulty', 'est_actif']
    search_fields = ['titre', 'chapitre__titre']
    ordering = ['chapitre']
    list_editable = ['est_actif']
    inlines = [CoursImageInline]


@admin.register(CoursImage)
class CoursImageAdmin(admin.ModelAdmin):
    list_display = ("id", "cours", "image_type", "position", "legende", "image_link")
    list_filter = ("image_type",)
    search_fields = ("cours__chapitre__titre", "legende")
    ordering = ("cours", "position", "id")

    def image_link(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html('<a href="{}" target="_blank">Voir</a>', obj.image.url)
            except Exception:
                return "(lien indisponible)"
        return "-"

    image_link.short_description = "Image"