"""
SYNTHESIS SHEETS - Fiches de synthèse
Fiches de résumé par chapitre pour faciliter les révisions
"""
from django.db import models
from core.models import BaseContent


class SynthesisSheet(BaseContent):
    """Une fiche de synthèse pour une notion"""

    ACCESS_SCOPE_PAID = 'paid'
    ACCESS_SCOPE_FREE = 'free'
    ACCESS_SCOPE_BOTH = 'both'
    ACCESS_SCOPE_CHOICES = [
        (ACCESS_SCOPE_PAID, 'Abonnés uniquement'),
        (ACCESS_SCOPE_FREE, 'Gratuit (découverte)'),
        (ACCESS_SCOPE_BOTH, 'Gratuit + Abonnés'),
    ]
    notion = models.ForeignKey(
        'curriculum.Notion', 
        on_delete=models.CASCADE, 
        related_name='synthesis_sheets'
    )
    
    # Contenu markdown de la fiche
    summary = models.TextField(
        verbose_name="Résumé",
        help_text="Contenu principal de la fiche en Markdown"
    )
    
    # Difficulté (ajouté manuellement au lieu d'hériter de BaseEducational)
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'), 
        ('hard', 'Difficile'),
    ]
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium',
        verbose_name="Difficulté"
    )
    
    # Points clés (optionnel, en JSON)
    key_points = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Points clés",
        help_text="Liste des points essentiels à retenir"
    )
    
    # Formules importantes (optionnel, en JSON)  
    formulas = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Formules",
        help_text="Formules mathématiques importantes"
    )
    
    # Exemples (optionnel, en JSON)
    examples = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Exemples",
        help_text="Exemples concrets d'application"
    )
    
    # Durée de lecture estimée en minutes
    reading_time_minutes = models.PositiveIntegerField(
        default=5,
        verbose_name="Temps de lecture (min)"
    )

    access_scope = models.CharField(
        max_length=10,
        choices=ACCESS_SCOPE_CHOICES,
        default=ACCESS_SCOPE_PAID,
        help_text="Définit si cette fiche est gratuite, payante ou visible dans les deux parcours."
    )
    
    class Meta:
        ordering = ['notion', 'titre']
        verbose_name = "Fiche de synthèse"
        verbose_name_plural = "Fiches de synthèse"
        unique_together = [['notion', 'titre']]

    def __str__(self):
        return f"Fiche - {self.notion.titre} - {self.titre}"

    @property
    def is_free_preview(self):
        return self.access_scope in {self.ACCESS_SCOPE_FREE, self.ACCESS_SCOPE_BOTH}


class SynthesisImage(models.Model):
    """Image associée à une fiche de synthèse"""
    TYPE_CHOICES = [
        ('illustration', 'Illustration'),
    ]

    sheet = models.ForeignKey(SynthesisSheet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='synthesis_images/')
    image_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='illustration')
    position = models.PositiveIntegerField(null=True, blank=True)
    caption = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sheet', 'position', 'id']
        verbose_name = "Image de fiche de synthèse"
        verbose_name_plural = "Images de fiches de synthèse"
        indexes = [
            models.Index(fields=['sheet', 'position']),
        ]

    def __str__(self):
        return f"Image {self.id} - Sheet {self.sheet_id}"
