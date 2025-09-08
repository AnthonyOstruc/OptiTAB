"""
COURS - ULTRA SIMPLE
Chaque chapitre a son cours
"""
from django.db import models
from core.models import BaseEducational
from django.db import models


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


class CoursImage(models.Model):
    """Image associée à un cours"""
    TYPE_CHOICES = [
        ('illustration', 'Illustration'),
    ]

    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cours_images/')
    image_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='illustration')
    position = models.PositiveIntegerField(null=True, blank=True)
    legende = models.CharField(max_length=255, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['cours', 'position', 'id']
        verbose_name = "Image de cours"
        verbose_name_plural = "Images de cours"
        indexes = [
            models.Index(fields=['cours', 'position']),
        ]

    def __str__(self):
        return f"Image {self.id} - Cours {self.cours_id}"