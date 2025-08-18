"""
COURS - ULTRA SIMPLE
Chaque chapitre a son cours
"""
from django.db import models
from core.models import BaseEducational


class Cours(BaseEducational):
    """Un cours pour un chapitre"""
    chapitre = models.OneToOneField(
        'curriculum.Chapitre', 
        on_delete=models.CASCADE, 
        related_name='cours'
    )
    video_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['chapitre']
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

    def __str__(self):
        return f"Cours - {self.chapitre.titre}"