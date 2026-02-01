"""
Modèles de base ultra-simplifiés avec gestionnaires optimisés
"""
from django.db import models
from django.utils import timezone
import uuid
from .services import BaseManager


class BaseModel(models.Model):
    """Modèle de base avec timestamps et statut actif"""
    est_actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    objects = BaseManager()
    
    class Meta:
        abstract = True


class BaseContent(BaseModel):
    """Pour le contenu avec titre et ordre"""
    titre = models.CharField(max_length=200, verbose_name="Titre")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        abstract = True
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre


class BaseSimple(BaseModel):
    """Pour le contenu simple - nom et ordre seulement"""
    nom = models.CharField(max_length=100, verbose_name="Nom")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        abstract = True
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom


class BaseEducational(BaseContent):
    """Pour le contenu éducatif (cours, exercices, quiz)"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'), 
        ('hard', 'Difficile'),
    ]
    
    contenu = models.TextField(verbose_name="Contenu")
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium',
        verbose_name="Difficulté"
    )
    
    class Meta:
        abstract = True


class BaseOrganizational(BaseContent):
    """Pour l'organisation (matières, thèmes, chapitres)"""
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    couleur = models.CharField(max_length=7, default='#3b82f6', verbose_name="Couleur")
    svg_icon = models.TextField(blank=True, null=True, verbose_name="Icône SVG")
    
    class Meta:
        abstract = True


class NewsletterSubscriber(BaseModel):
    """Abonnés à la newsletter avec lien de désinscription.

    - Utilise `est_actif` hérité pour l'état d'abonnement (True = abonné)
    - Conserve un `unsubscribe_token` unique pour les liens dans les emails
    - Garde des métadonnées utiles (source, IP, timestamps)
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=120, blank=True, default="", verbose_name="Prénom")
    last_name = models.CharField(max_length=120, blank=True, default="", verbose_name="Nom")
    source = models.CharField(max_length=50, default='website', verbose_name="Source")
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="Jeton de désinscription")
    unsubscribed_at = models.DateTimeField(null=True, blank=True, verbose_name="Désabonné le")
    last_email_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Dernier email envoyé")
    consent_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP de consentement")

    objects = BaseManager()

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"
        ordering = ['-date_creation']

    def __str__(self):
        return self.email

    # Helpers
    def mark_unsubscribed(self, save=True):
        self.est_actif = False
        self.unsubscribed_at = timezone.now()
        if save:
            self.save(update_fields=['est_actif', 'unsubscribed_at', 'date_modification'])

    def reactivate(self, save=True):
        self.est_actif = True
        self.unsubscribed_at = None
        if save:
            self.save(update_fields=['est_actif', 'unsubscribed_at', 'date_modification'])
