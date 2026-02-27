from django.contrib import admin
from django.utils.html import format_html

from .models import SynthesisImage, SynthesisSheet
from .utils import resolve_synthesis_image_alt, resolve_synthesis_image_title, resolve_synthesis_title


class SynthesisImageInline(admin.TabularInline):
    model = SynthesisImage
    extra = 0
    fields = (
        'preview',
        'image',
        'image_type',
        'position',
        'alt_text',
        'title_text',
        'caption',
        'width',
        'height',
    )
    readonly_fields = ('preview', 'width', 'height')
    can_delete = True

    def preview(self, obj):
        if getattr(obj, 'image', None):
            try:
                return format_html(
                    '<img src="{}" style="height: 80px; max-width: 140px; object-fit: cover;" />',
                    obj.image.url,
                )
            except Exception:
                return "(apercu indisponible)"
        return '-'

    preview.short_description = 'Apercu'


@admin.register(SynthesisSheet)
class SynthesisSheetAdmin(admin.ModelAdmin):
    list_display = (
        'titre',
        'notion',
        'get_matiere',
        'sheet_type',
        'reading_time_minutes',
        'access_scope',
        'est_actif',
        'date_creation',
    )
    list_filter = (
        'difficulty',
        'sheet_type',
        'access_scope',
        'est_actif',
        'notion__theme__matiere',
        'date_creation',
    )
    search_fields = ('titre', 'notion__titre', 'summary')
    ordering = ('notion', 'ordre', 'titre')
    inlines = [SynthesisImageInline]

    fieldsets = (
        (None, {
            'fields': ('titre', 'notion', 'ordre', 'difficulty', 'sheet_type', 'access_scope', 'est_actif')
        }),
        ('Contenu', {
            'fields': ('summary', 'reading_time_minutes'),
            'classes': ('wide',)
        }),
        ('Donnees structurees', {
            'fields': ('key_points', 'formulas', 'examples'),
            'classes': ('collapse',)
        }),
    )

    def get_matiere(self, obj):
        return obj.notion.theme.matiere.titre if obj.notion and obj.notion.theme and obj.notion.theme.matiere else '-'

    get_matiere.short_description = 'Matiere'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'notion',
            'notion__theme',
            'notion__theme__matiere'
        )


@admin.register(SynthesisImage)
class SynthesisImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sheet',
        'image_type',
        'position',
        'alt_text',
        'title_text',
        'caption',
        'image_link',
    )
    list_filter = ('image_type',)
    search_fields = ('sheet__titre', 'caption', 'alt_text', 'title_text', 'image')
    ordering = ('sheet', 'position', 'id')
    list_editable = ('position', 'alt_text', 'title_text', 'caption')
    actions = ('auto_fill_alt_from_filename_legend',)

    def image_link(self, obj):
        if getattr(obj, 'image', None):
            try:
                return format_html('<a href="{}" target="_blank">Voir</a>', obj.image.url)
            except Exception:
                return "(lien indisponible)"
        return '-'

    image_link.short_description = 'Image'

    @admin.action(description='Auto-fill alt from filename/legend')
    def auto_fill_alt_from_filename_legend(self, request, queryset):
        updated_count = 0

        for image_obj in queryset.select_related('sheet', 'sheet__notion'):
            updates = []
            synthesis_title = resolve_synthesis_title(getattr(image_obj, 'sheet', None))

            if not str(image_obj.alt_text or '').strip():
                image_obj.alt_text = resolve_synthesis_image_alt(
                    image_obj,
                    synthesis_title=synthesis_title
                )
                updates.append('alt_text')

            if not str(image_obj.title_text or '').strip():
                title_value = resolve_synthesis_image_title(image_obj)
                if title_value:
                    image_obj.title_text = title_value
                    updates.append('title_text')

            if (not image_obj.width or not image_obj.height) and getattr(image_obj, 'image', None):
                try:
                    if not image_obj.width:
                        image_obj.width = int(getattr(image_obj.image, 'width', 0) or 0) or None
                        updates.append('width')
                    if not image_obj.height:
                        image_obj.height = int(getattr(image_obj.image, 'height', 0) or 0) or None
                        updates.append('height')
                except Exception:
                    pass

            if updates:
                image_obj.save(update_fields=updates + ['date_modification'])
                updated_count += 1

        self.message_user(request, f'{updated_count} image(s) mises a jour.')
