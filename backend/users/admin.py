"""
Configuration Admin pour l'utilisateur personnalisé - Version simplifiée
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from .models import CustomUser, UserFavoriteMatiere, UserSelectedMatiere, ParentChild
from subscriptions.models import UserSubscription, AccessPass
from subscriptions.permissions import user_has_any_manual_access


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Administration simplifiée pour les utilisateurs"""
    model = CustomUser

    # Champs d'identification (remplace username par email)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    # Colonnes affichées dans la liste
    list_display = (
        'email',
        'full_name',
        'role',
        'civilite',
        'telephone',
        'pays',
        'niveau_pays',
        'subscription_plan_display',
        'subscription_status_display',
        'has_complimentary_access',
        'complimentary_access_scope_display',
        'complimentary_access_window_display',
        'is_active',
        'is_staff',
        'date_joined',
    )

    # Filtres disponibles
    list_filter = (
        'is_staff',
        'is_active',
        'civilite',
        'pays',
        'niveau_pays',
        'has_complimentary_access',
        'complimentary_access_levels',
        'complimentary_access_starts_at',
        'complimentary_access_ends_at',
        'date_joined',
    )

    # Champs de recherche
    search_fields = ('email', 'first_name', 'last_name', 'telephone')

    # Ordre d'affichage
    ordering = ('-date_joined',)

    # Organisation des champs en sections
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'civilite', 'date_naissance', 'telephone', 'role')
        }),
        ('Géographie éducative', {
            'fields': ('pays', 'niveau_pays'),
            'classes': ('collapse',)
        }),
        ('Gamification', {
            'fields': ('xp',),
            'classes': ('collapse',)
        }),
        ('Accès premium', {
            'fields': (
                'has_complimentary_access',
                'complimentary_access_levels',
                'complimentary_access_starts_at',
                'complimentary_access_ends_at',
            ),
        }),
        ('Abonnement / Pass', {
            'fields': (
                'subscription_plan_display',
                'subscription_status_display',
                'subscription_ends_display',
                'subscription_has_active_pass',
            ),
            'classes': ('collapse',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Vérification', {
            'fields': ('verification_code',),
            'classes': ('collapse',)
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = UserAdmin.readonly_fields + (
        'subscription_plan_display',
        'subscription_status_display',
        'subscription_ends_display',
        'subscription_has_active_pass',
    )
    filter_horizontal = ('complimentary_access_levels',)

    def _get_subscription(self, obj):
        try:
            return obj.subscription
        except UserSubscription.DoesNotExist:
            return None

    def subscription_plan_display(self, obj):
        subscription = self._get_subscription(obj)
        if subscription and subscription.plan:
            billing = subscription.plan.get_billing_period_display() if hasattr(subscription.plan, 'get_billing_period_display') else subscription.plan.billing_period
            return f"{subscription.plan.name} ({billing})"
        if user_has_any_manual_access(obj):
            return 'Accès manuel'
        return '—'

    subscription_plan_display.short_description = 'Plan'

    def subscription_status_display(self, obj):
        subscription = self._get_subscription(obj)
        if subscription:
            try:
                return subscription.get_status_display()
            except AttributeError:
                return subscription.status
        if user_has_any_manual_access(obj):
            return 'Accès manuel'
        return 'Aucun'

    subscription_status_display.short_description = 'Statut'

    def complimentary_access_scope_display(self, obj):
        levels_count = obj.complimentary_access_levels.count()
        if levels_count > 0:
            return f"Niveaux ({levels_count})"
        if obj.has_complimentary_access:
            return 'Global'
        return 'Aucun'

    complimentary_access_scope_display.short_description = "Portée accès offert"

    def complimentary_access_window_display(self, obj):
        starts_at = self._format_dt(getattr(obj, 'complimentary_access_starts_at', None))
        ends_at = self._format_dt(getattr(obj, 'complimentary_access_ends_at', None))
        if starts_at and ends_at:
            return f"{starts_at} -> {ends_at}"
        if starts_at:
            return f"A partir du {starts_at}"
        if ends_at:
            return f"Jusqu'au {ends_at}"
        return "Toujours"

    complimentary_access_window_display.short_description = "Validité accès offert"

    @staticmethod
    def _format_dt(dt):
        if not dt:
            return None
        try:
            aware = timezone.localtime(dt) if timezone.is_aware(dt) else dt
            return aware.strftime('%d/%m/%Y %H:%M')
        except Exception:
            return str(dt)

    def subscription_ends_display(self, obj):
        subscription = self._get_subscription(obj)
        if subscription and subscription.current_period_end:
            return self._format_dt(subscription.current_period_end)
        pass_obj = AccessPass.objects.filter(user=obj).order_by('-ends_at').first()
        if pass_obj:
            formatted = self._format_dt(pass_obj.ends_at)
            return f"Pass jusqu'au {formatted}" if formatted else 'Pass actif'
        return '—'

    subscription_ends_display.short_description = 'Expire le'

    def subscription_has_active_pass(self, obj):
        now = timezone.now()
        return AccessPass.objects.filter(user=obj, ends_at__gt=now).exists()

    subscription_has_active_pass.short_description = 'Pass actif'
    subscription_has_active_pass.boolean = True


@admin.register(ParentChild)
class ParentChildAdmin(admin.ModelAdmin):
    list_display = ('parent', 'child', 'created_at')
    search_fields = ('parent__email', 'child__email')
    list_filter = ('created_at',)



@admin.register(UserFavoriteMatiere)
class UserFavoriteMatiereAdmin(admin.ModelAdmin):
    """Administration des matières favorites"""
    list_display = ('user', 'matiere', 'created_at')
    list_filter = ('created_at', 'matiere')
    search_fields = ('user__email', 'matiere__titre')
    ordering = ('-created_at',)


@admin.register(UserSelectedMatiere)
class UserSelectedMatiereAdmin(admin.ModelAdmin):
    """Administration des matières sélectionnées"""
    list_display = ('user', 'matiere', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'matiere')
    search_fields = ('user__email', 'matiere__titre')
    ordering = ('user', 'order')
