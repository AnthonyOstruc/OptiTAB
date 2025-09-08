"""
Modèles de base ultra-simplifiés avec gestionnaires optimisés
"""
from django.db import models
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
