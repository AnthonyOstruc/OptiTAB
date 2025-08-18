"""
FICHES - ULTRA SIMPLE
Fiches de synthèse pour les notions
"""
from django.db import models
from core.models import BaseContent


class FicheSynthese(BaseContent):
    """Une fiche de synthèse pour une notion"""
    notion = models.OneToOneField(
        'curriculum.Notion', 
        on_delete=models.CASCADE, 
        related_name='fiche'
    )
    contenu_markdown = models.TextField()
    
    class Meta:
        ordering = ['notion']
        verbose_name = "Fiche de Synthèse"
        verbose_name_plural = "Fiches de Synthèse"

    def __str__(self):
        return f"Fiche - {self.notion.titre}"