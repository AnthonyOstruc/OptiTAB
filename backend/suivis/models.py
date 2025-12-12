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


class QuizSubmission(BaseModel):
    """Soumission manuelle de quiz par les élèves (envoyé par WhatsApp)"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('graded', 'Noté'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE, related_name='submissions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Note attribuée par l'admin (sur 20)
    note = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Note sur 20")
    
    # Commentaire de correction de l'admin
    commentaire = models.TextField(blank=True, default='', help_text="Commentaire de correction")
    
    # Informations sur la correction
    corrige_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='quiz_corriges',
        help_text="Administrateur qui a corrigé"
    )
    date_correction = models.DateTimeField(null=True, blank=True, help_text="Date de correction")
    
    # Notes pour l'admin (numéro WhatsApp, date de réception, etc.)
    notes_admin = models.TextField(blank=True, default='', help_text="Notes privées pour l'admin")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Soumission de quiz"
        verbose_name_plural = "Soumissions de quiz"
        unique_together = [['user', 'quiz']]
    
    def __str__(self):
        return f"{self.user.email} - {self.quiz.titre} - {self.get_status_display()}"