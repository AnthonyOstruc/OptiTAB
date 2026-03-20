"""
Admin du blog OptiTAB — interface complète pour gérer les articles
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import BlogCategory, BlogTag, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'ordre', 'est_actif', 'date_creation']
    list_editable = ['ordre', 'est_actif']
    list_filter = ['est_actif']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    ordering = ['ordre', 'nom']


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'est_actif']
    list_filter = ['est_actif']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}
    ordering = ['nom']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'titre', 'categorie', 'auteur', 'statut_display', 'date_publication',
        'ordre', 'reading_time_display', 'est_actif'
    ]
    list_editable = ['ordre', 'est_actif']
    list_filter = ['statut', 'est_actif', 'categorie', 'tags', 'date_publication']
    search_fields = ['titre', 'extrait', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}
    autocomplete_fields = ['categorie', 'auteur']
    filter_horizontal = ['tags', 'articles_lies']
    readonly_fields = ['date_creation', 'date_modification', 'reading_time_display', 'image_preview']
    date_hierarchy = 'date_publication'
    ordering = ['-date_publication', '-date_creation']

    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'extrait', 'contenu', 'image_couverture', 'image_preview')
        }),
        ('Organisation', {
            'fields': ('categorie', 'tags', 'auteur', 'articles_lies')
        }),
        ('Publication', {
            'fields': ('statut', 'date_publication', 'ordre', 'est_actif')
        }),
        ('SEO', {
            'fields': ('seo_title', 'meta_description', 'og_title', 'og_description'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification', 'reading_time_display'),
            'classes': ('collapse',)
        }),
    )

    def statut_display(self, obj):
        colors = {'draft': '#f59e0b', 'published': '#10b981'}
        labels = {'draft': 'Brouillon', 'published': 'Publié'}
        color = colors.get(obj.statut, '#6b7280')
        label = labels.get(obj.statut, obj.statut)
        return format_html('<span style="color:{};">● {}</span>', color, label)
    statut_display.short_description = 'Statut'

    def reading_time_display(self, obj):
        return f'{obj.reading_time} min'
    reading_time_display.short_description = 'Temps de lecture'

    def image_preview(self, obj):
        if obj.image_couverture:
            return format_html(
                '<img src="{}" style="max-height:200px;max-width:400px;border-radius:8px;" />',
                obj.image_couverture.url
            )
        return '—'
    image_preview.short_description = 'Aperçu image'

    def save_model(self, request, obj, form, change):
        if not obj.auteur_id:
            obj.auteur = request.user
        super().save_model(request, obj, form, change)
