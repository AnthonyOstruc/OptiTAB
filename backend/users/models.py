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
    
    # Partage de l'historique avec les parents
    share_history_with_parents = models.BooleanField(
        default=False,
        verbose_name="Partager l'historique avec les parents",
        help_text="Autoriser les parents à voir l'historique d'apprentissage"
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
    verification_code = models.CharField(max_length=128, blank=True, null=True)
    verification_code_sent_at = models.DateTimeField(null=True, blank=True)
    pending_email = models.EmailField(null=True, blank=True, unique=False)
    pending_email_token = models.CharField(max_length=128, blank=True, null=True)
    pending_email_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps automatiques
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Gamification
    xp = models.PositiveIntegerField(default=0, verbose_name="Points d'expérience")

    # Daily login streak
    login_streak_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Série de connexions (jours consécutifs)",
        help_text="Nombre de jours consécutifs connectés"
    )
    login_streak_last_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Dernière date de récompense quotidienne",
        help_text="Dernière date (locale) où la récompense quotidienne a été attribuée"
    )
    has_complimentary_access = models.BooleanField(
        default=False,
        verbose_name="Accès premium offert",
        help_text="Autorise l'accès aux contenus premium sans abonnement actif ou pass."
    )

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

    @property
    def subscription(self):
        """
        Retourne l'abonnement principal (actif) de l'utilisateur.
        Compatible avec l'ancien champ OneToOne.
        """
        try:
            subscriptions_manager = getattr(self, 'subscriptions', None)
            if subscriptions_manager is None:
                from subscriptions.models import UserSubscription
                queryset = UserSubscription.objects.filter(user=self)
            else:
                queryset = subscriptions_manager.all()
            return (
                queryset.filter(status__in=['active', 'trialing'])
                .order_by('-created_at')
                .first()
                or queryset.order_by('-created_at').first()
            )
        except Exception:
            return None


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
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DECLINED = 'declined'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_DECLINED, 'Declined'),
    ]

    parent = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name='children_links'
    )
    child = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name='parent_links'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('parent', 'child')
        indexes = [
            models.Index(fields=['parent', 'child']),
            models.Index(fields=['parent', 'status']),
            models.Index(fields=['child', 'status']),
        ]
        verbose_name = 'Lien parent-enfant'
        verbose_name_plural = 'Liens parents-enfants'
    
    def __str__(self):
        return f"{self.parent.email} → {self.child.email} ({self.status})"

    def mark_accepted(self):
        self.status = self.STATUS_ACCEPTED
        self.responded_at = timezone.now()
        self.save(update_fields=['status', 'responded_at', 'updated_at'] if hasattr(self, 'updated_at') else ['status', 'responded_at'])

    def mark_declined(self):
        self.status = self.STATUS_DECLINED
        self.responded_at = timezone.now()
        self.save(update_fields=['status', 'responded_at', 'updated_at'] if hasattr(self, 'updated_at') else ['status', 'responded_at'])


class UserNotification(models.Model):
    """Notification persistante liée à un utilisateur"""
    TYPE_CHOICES = [
        ('xp_gained', 'XP Gained'),
        ('level_up', 'Level Up'),
        ('exercise_unlocked', 'Exercise Unlocked'),
        ('chapter_completed', 'Chapter Completed'),
        ('achievement', 'Achievement'),
        ('parent_invite', 'Parent Invite'),
        ('parent_invite_response', 'Parent Invite Response'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at', '-id']
        indexes = [
            models.Index(fields=['user', 'read', '-created_at']),
        ]

    def __str__(self):
        return f"Notification {self.type} → {self.user.email}"
