"""
Core admin functionality providing consistent admin interface patterns.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


class BaseModelAdmin(admin.ModelAdmin):
    """
    Base admin class with common functionality for all models.
    """
    
    # Common fields that appear in most models
    readonly_fields = ['date_creation', 'date_modification']
    
    # Common list display fields
    base_list_display = ['__str__']
    
    # Common search fields
    search_fields = ['titre', 'nom']
    
    # Common filters
    list_filter = ['est_actif', 'date_creation', 'date_modification']
    
    # Default ordering
    ordering = ['date_creation']

    def get_list_display(self, request):
        """
        Dynamically build list_display based on model fields.
        """
        model_fields = [f.name for f in self.model._meta.fields]
        display_fields = []
        
        # Add primary identifier
        if 'titre' in model_fields:
            display_fields.append('titre')
        elif 'nom' in model_fields:
            display_fields.append('nom')
        else:
            display_fields.append('__str__')
        
        # Add status fields
        if 'est_actif' in model_fields:
            display_fields.append('status_display')
        
        # Add timestamps
        if 'date_creation' in model_fields:
            display_fields.append('date_creation')
        
        return display_fields
    
    def get_list_filter(self, request):
        """
        Dynamically build list_filter based on model fields.
        """
        model_fields = [f.name for f in self.model._meta.fields]
        filters = []
        
        if 'est_actif' in model_fields:
            filters.append('est_actif')
        if 'difficulty' in model_fields:
            filters.append('difficulty')
        if 'date_creation' in model_fields:
            filters.append('date_creation')
        
        return filters
    
    def get_search_fields(self, request):
        """
        Dynamically build search_fields based on model fields.
        """
        model_fields = [f.name for f in self.model._meta.fields]
        search_fields = []
        
        if 'titre' in model_fields:
            search_fields.append('titre')
        if 'nom' in model_fields:
            search_fields.append('nom')

        
        return search_fields
    
    def status_display(self, obj):
        """
        Display active status with visual indicator.
        """
        if hasattr(obj, 'est_actif'):
            if obj.est_actif:
                return format_html(
                    '<span style="color: green;">●</span> Actif'
                )
            else:
                return format_html(
                    '<span style="color: red;">●</span> Inactif'
                )
        return '-'
    
    status_display.short_description = _('Statut')
    
    def get_fieldsets(self, request, obj=None):
        """
        Organize fields into logical fieldsets.
        """
        model_fields = [f.name for f in self.model._meta.fields]
        fieldsets = []
        
        # Basic information
        basic_fields = []
        for field in ['titre', 'nom']:
            if field in model_fields:
                basic_fields.append(field)
        
        if basic_fields:
            fieldsets.append((_('Informations de base'), {
                'fields': basic_fields
            }))
        
        # Configuration
        config_fields = []
        for field in ['ordre', 'couleur', 'difficulty', 'svg_icon']:
            if field in model_fields:
                config_fields.append(field)
        
        if config_fields:
            fieldsets.append((_('Configuration'), {
                'fields': config_fields,
                'classes': ['collapse']
            }))
        
        # Status and metadata
        status_fields = []
        for field in ['est_actif']:
            if field in model_fields:
                status_fields.append(field)
        
        status_fields.extend(['date_creation', 'date_modification'])
        
        fieldsets.append((_('Statut et métadonnées'), {
            'fields': status_fields,
            'classes': ['collapse']
        }))
        
        return fieldsets


class ActiveModelAdmin(BaseModelAdmin):
    """
    Admin for models with active/inactive functionality.
    """
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        """
        Mark selected objects as active.
        """
        updated = queryset.update(est_actif=True)
        self.message_user(
            request,
            f'{updated} élément(s) activé(s) avec succès.'
        )
    
    make_active.short_description = _('Activer les éléments sélectionnés')
    
    def make_inactive(self, request, queryset):
        """
        Mark selected objects as inactive.
        """
        updated = queryset.update(est_actif=False)
        self.message_user(
            request,
            f'{updated} élément(s) désactivé(s) avec succès.'
        )
    
    make_inactive.short_description = _('Désactiver les éléments sélectionnés')


class OrderedModelAdmin(BaseModelAdmin):
    """
    Admin for models with ordering functionality.
    """
    
    list_editable = ['ordre']
    
    def get_ordering(self, request):
        """
        Default ordering by ordre field.
        """
        return ['ordre']


class ContentModelAdmin(ActiveModelAdmin, OrderedModelAdmin):
    """
    Admin for content models with full functionality.
    """
    
    def get_list_display(self, request):
        """
        Enhanced list display for content models.
        """
        display = super().get_list_display(request)
        
        # Add order field if available
        if hasattr(self.model, 'ordre'):
            if 'ordre' not in display:
                display.insert(-1, 'ordre')
        
        return display


class ReadOnlyModelAdmin(BaseModelAdmin):
    """
    Admin for read-only models.
    """
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
