"""
SYNTHESIS SHEETS - Fiches de synthèse
Fiches de résumé par chapitre pour faciliter les révisions
"""
from django.db import models
from core.models import BaseContent


class SynthesisSheet(BaseContent):
    """Une fiche de synthèse pour une notion"""
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
    
    class Meta:
        ordering = ['notion', 'ordre']
        verbose_name = "Fiche de synthèse"
        verbose_name_plural = "Fiches de synthèse"
        unique_together = [['notion', 'titre']]

    def __str__(self):
        return f"Fiche - {self.notion.titre} - {self.titre}"
