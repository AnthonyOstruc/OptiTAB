"""
QUIZ - ULTRA SIMPLE
Chaque chapitre a ses quiz
"""
from django.db import models
from core.models import BaseEducational


class Quiz(BaseEducational):
    """Un quiz pour une notion"""
    notion = models.ForeignKey(
        'curriculum.Notion', 
        on_delete=models.CASCADE, 
        related_name='quiz',
        null=True  # Temporaire pour migration
    )
    questions_data = models.JSONField(default=list)  # Questions en JSON
    duree_minutes = models.PositiveIntegerField(default=30)
    solution = models.TextField(
        blank=True, 
        default='', 
        verbose_name="Solution du quiz",
        help_text="Solution complète du quiz, visible par l'élève après correction"
    )
    
    class Meta:
        ordering = ['notion', 'ordre']
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"

    def __str__(self):
        return f"Quiz - {self.notion.titre} - {self.titre}"


class QuizImage(models.Model):
    """Image associée à un quiz (question ou réponse)"""
    TYPE_CHOICES = [
        ('question', 'Question'),
        ('answer', 'Réponse'),
        ('illustration', 'Illustration'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='quiz_images/')
    image_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='question')
    position = models.PositiveIntegerField(null=True, blank=True)
    legende = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['quiz', 'position', 'id']
        verbose_name = "Image de quiz"
        verbose_name_plural = "Images de quiz"
        indexes = [
            models.Index(fields=['quiz', 'position']),
        ]

    def __str__(self):
        return f"Image {self.id} - Quiz {self.quiz_id}"