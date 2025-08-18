"""
SUIVIS - ULTRA SIMPLE
Pour sauvegarder ce que l'utilisateur a fait
"""
from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel

User = get_user_model()


class SuiviExercice(BaseModel):
    """Suivi des exercices par utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercice = models.ForeignKey('curriculum.Exercice', on_delete=models.CASCADE)
    reponse_donnee = models.TextField()
    est_correct = models.BooleanField(default=False)
    points_obtenus = models.PositiveIntegerField(default=0)
    temps_seconde = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'exercice']
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.user.email} - {self.exercice.titre}"


class SuiviQuiz(BaseModel):
    """Suivi des quiz par utilisateur - permet plusieurs tentatives"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    temps_total_seconde = models.PositiveIntegerField(default=0)
    tentative_numero = models.PositiveIntegerField(default=1)
    xp_gagne = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'quiz', 'tentative_numero']
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.user.email} - {self.quiz.titre} - Tentative {self.tentative_numero}"