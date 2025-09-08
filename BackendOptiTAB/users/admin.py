"""
Configuration Admin pour l'utilisateur personnalisé - Version simplifiée
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserFavoriteMatiere, UserSelectedMatiere, ParentChild


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
    list_display = ('email', 'full_name', 'role', 'civilite', 'telephone', 'pays', 'niveau_pays', 'is_active', 'is_staff', 'date_joined')

    # Filtres disponibles
    list_filter = ('is_staff', 'is_active', 'civilite', 'pays', 'niveau_pays', 'date_joined')

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
