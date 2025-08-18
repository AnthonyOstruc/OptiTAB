"""
QUIZ - ULTRA SIMPLE
Chaque chapitre a ses quiz
"""
from django.db import models
from core.models import BaseEducational


class Quiz(BaseEducational):
    """Un quiz pour un chapitre"""
    chapitre = models.ForeignKey(
        'curriculum.Chapitre', 
        on_delete=models.CASCADE, 
        related_name='quiz'
    )
    questions_data = models.JSONField(default=list)  # Questions en JSON
    duree_minutes = models.PositiveIntegerField(default=30)
    
    class Meta:
        ordering = ['chapitre', 'ordre']
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"

    def __str__(self):
        return f"Quiz - {self.chapitre.titre} - {self.titre}"