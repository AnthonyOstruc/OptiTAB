"""
Core admin functionality providing consistent admin interface patterns.
"""
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone

from .models import NewsletterSubscriber, DiagnosticLead


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


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(BaseModelAdmin):
    list_display = ('email', 'est_actif', 'date_creation', 'unsubscribed_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('est_actif', 'source', 'date_creation')
    readonly_fields = ('unsubscribe_token', 'date_creation', 'date_modification')

    fieldsets = (
        (_('Abonné'), {
            'fields': ('email', 'first_name', 'last_name', 'source', 'est_actif')
        }),
        (_('Données'), {
            'classes': ('collapse',),
            'fields': ('consent_ip', 'last_email_sent_at')
        }),
        (_('Désinscription'), {
            'classes': ('collapse',),
            'fields': ('unsubscribed_at', 'unsubscribe_token')
        }),
        (_('Métadonnées'), {
            'classes': ('collapse',),
            'fields': ('date_creation', 'date_modification')
        }),
    )


@admin.register(DiagnosticLead)
class DiagnosticLeadAdmin(admin.ModelAdmin):
    """Admin pour consulter et exporter les leads du diagnostic gratuit."""

    list_display = (
        'email',
        'first_name',
        'level',
        'difficulty',
        'consent_email_marketing',
        'diagnostic_sent_at',
        'utm_source',
        'date_creation',
    )
    list_filter = (
        'level',
        'difficulty',
        'consent_email_marketing',
        'form_location',
        'utm_source',
        'utm_campaign',
        'date_creation',
    )
    search_fields = (
        'email',
        'first_name',
        'utm_campaign',
        'utm_source',
        'gclid',
        'fbclid',
    )
    readonly_fields = (
        'date_creation',
        'date_modification',
        'consent_timestamp',
        'consent_ip',
        'referrer',
        'landing_path',
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_content',
        'utm_term',
        'gclid',
        'fbclid',
        'ttclid',
        'msclkid',
        'linked_subscriber_link',
    )
    list_select_related = ('linked_subscriber',)
    date_hierarchy = 'date_creation'
    ordering = ('-date_creation',)
    list_per_page = 50
    actions = ['export_as_csv', 'mark_diagnostic_sent']

    fieldsets = (
        (_('Lead'), {
            'fields': ('email', 'first_name', 'level', 'difficulty', 'form_location', 'lead_magnet')
        }),
        (_('Consentement RGPD'), {
            'fields': ('consent_email_marketing', 'consent_timestamp', 'consent_ip'),
            'description': _("Trace du consentement marketing email (obligatoire RGPD).")
        }),
        (_('Newsletter'), {
            'fields': ('linked_subscriber_link', 'diagnostic_sent_at')
        }),
        (_('Acquisition / Attribution'), {
            'classes': ('collapse',),
            'fields': (
                'landing_path',
                'referrer',
                'utm_source',
                'utm_medium',
                'utm_campaign',
                'utm_content',
                'utm_term',
                'gclid',
                'fbclid',
                'ttclid',
                'msclkid',
            )
        }),
        (_('Métadonnées'), {
            'classes': ('collapse',),
            'fields': ('est_actif', 'date_creation', 'date_modification')
        }),
    )

    def linked_subscriber_link(self, obj):
        if not obj.linked_subscriber_id:
            return '—'
        url = reverse('admin:core_newslettersubscriber_change', args=[obj.linked_subscriber_id])
        return format_html('<a href="{}">{}</a>', url, obj.linked_subscriber.email)

    linked_subscriber_link.short_description = _('Abonné newsletter associé')

    def export_as_csv(self, request, queryset):
        """Télécharge la sélection au format CSV (UTF-8 BOM pour Excel)."""
        filename = f"diagnostic_leads_{timezone.now().strftime('%Y%m%d_%H%M')}.csv"
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write('﻿')  # BOM UTF-8 pour Excel

        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'date_creation',
            'email',
            'first_name',
            'level',
            'difficulty',
            'consent_email_marketing',
            'consent_timestamp',
            'consent_ip',
            'form_location',
            'lead_magnet',
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_content',
            'utm_term',
            'gclid',
            'fbclid',
            'ttclid',
            'msclkid',
            'referrer',
            'landing_path',
            'linked_subscriber_email',
            'diagnostic_sent_at',
        ])

        for lead in queryset.select_related('linked_subscriber').iterator():
            writer.writerow([
                lead.date_creation.isoformat() if lead.date_creation else '',
                lead.email,
                lead.first_name,
                lead.get_level_display(),
                lead.get_difficulty_display(),
                'oui' if lead.consent_email_marketing else 'non',
                lead.consent_timestamp.isoformat() if lead.consent_timestamp else '',
                lead.consent_ip or '',
                lead.get_form_location_display(),
                lead.lead_magnet,
                lead.utm_source,
                lead.utm_medium,
                lead.utm_campaign,
                lead.utm_content,
                lead.utm_term,
                lead.gclid,
                lead.fbclid,
                lead.ttclid,
                lead.msclkid,
                lead.referrer,
                lead.landing_path,
                lead.linked_subscriber.email if lead.linked_subscriber_id else '',
                lead.diagnostic_sent_at.isoformat() if lead.diagnostic_sent_at else '',
            ])

        self.message_user(request, f"{queryset.count()} lead(s) exporté(s).")
        return response

    export_as_csv.short_description = _("Exporter la sélection en CSV")

    def mark_diagnostic_sent(self, request, queryset):
        """Marque les leads sélectionnés comme ayant reçu leur diagnostic."""
        now = timezone.now()
        updated = queryset.filter(diagnostic_sent_at__isnull=True).update(
            diagnostic_sent_at=now,
            date_modification=now,
        )
        self.message_user(request, f"{updated} lead(s) marqué(s) comme diagnostic envoyé.")

    mark_diagnostic_sent.short_description = _("Marquer comme diagnostic envoyé")
