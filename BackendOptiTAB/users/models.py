from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Gestionnaire simplifié pour utilisateurs"""
    
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Utilisateur complet avec informations personnelles"""
    
    # Champs essentiels
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Rôle (élève/parent) pour personnaliser l'expérience
    role = models.CharField(
        max_length=20,
        choices=[('student', 'Étudiant'), ('parent', 'Parent')],
        default='student',
        db_index=True
    )
    
    # Informations personnelles ajoutées
    civilite = models.CharField(max_length=10, choices=[('M', 'Monsieur'), ('Mme', 'Madame')], null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Numéro de téléphone")
    
    # Géographie éducative (optionnel)
    pays = models.ForeignKey('pays.Pays', on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    niveau_pays = models.ForeignKey('pays.Niveau', on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    
    # Statuts
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    # Vérification email
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
    # Timestamps automatiques
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Gamification
    xp = models.PositiveIntegerField(default=0, verbose_name="Points d'expérience")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def niveau(self):
        """Compatibilité avec l'ancien code"""
        return self.niveau_pays


# Modèle pour sauvegarder les matières favorites de l'utilisateur
class UserFavoriteMatiere(models.Model):
    user = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE, 
        related_name='favorite_matieres',
        verbose_name="Utilisateur"
    )
    matiere = models.ForeignKey(
        'curriculum.Matiere', 
        on_delete=models.CASCADE,
        verbose_name="Matière"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        verbose_name = "Matière favorite"
        verbose_name_plural = "Matières favorites"
        unique_together = ('user', 'matiere')  # Un utilisateur ne peut favoriser qu'une fois la même matière
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.email} - {self.matiere.titre}"


# Modèle pour sauvegarder les matières sélectionnées par l'utilisateur
class UserSelectedMatiere(models.Model):
    user = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE, 
        related_name='selected_matieres',
        verbose_name="Utilisateur"
    )
    matiere = models.ForeignKey(
        'curriculum.Matiere', 
        on_delete=models.CASCADE,
        verbose_name="Matière"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Ordre d'affichage des onglets (0 = premier)"
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Onglet actif",
        help_text="Indique si c'est l'onglet actuellement sélectionné"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Matière sélectionnée"
        verbose_name_plural = "Matières sélectionnées"
        unique_together = ('user', 'matiere')  # Un utilisateur ne peut sélectionner qu'une fois la même matière
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.user.email} - {self.matiere.titre} (ordre: {self.order})"

    def save(self, *args, **kwargs):
        # Si cet onglet devient actif, désactiver tous les autres pour cet utilisateur
        if self.is_active:
            UserSelectedMatiere.objects.filter(user=self.user).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class ParentChild(models.Model):
    """Lien parent-enfant: un parent peut suivre plusieurs élèves."""
    parent = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name='children_links'
    )
    child = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name='parent_links'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('parent', 'child')
        indexes = [
            models.Index(fields=['parent', 'child']),
        ]
        verbose_name = 'Lien parent-enfant'
        verbose_name_plural = 'Liens parents-enfants'
    
    def __str__(self):
        return f"{self.parent.email} → {self.child.email}"
