"""
COURS - ULTRA SIMPLE
Chaque chapitre a son cours
"""
from django.db import models
from core.models import BaseEducational


class Cours(BaseEducational):
    """Un cours pour une notion"""
    ACCESS_SCOPE_PAID = 'paid'
    ACCESS_SCOPE_FREE = 'free'
    ACCESS_SCOPE_BOTH = 'both'
    ACCESS_SCOPE_CHOICES = [
        (ACCESS_SCOPE_PAID, 'Abonnés uniquement'),
        (ACCESS_SCOPE_FREE, 'Gratuit (découverte)'),
        (ACCESS_SCOPE_BOTH, 'Gratuit + Abonnés'),
    ]

    notion = models.OneToOneField(
        'curriculum.Notion',
        on_delete=models.CASCADE,
        related_name='cours',
        null=True  # Temporaire pour migration
    )
    video_url = models.URLField(blank=True, null=True)
    # PDF optionnel associé au cours (uploadé manuellement via l'admin)
    pdf_file = models.FileField(upload_to='cours_pdfs/', blank=True, null=True)
    access_scope = models.CharField(
        max_length=10,
        choices=ACCESS_SCOPE_CHOICES,
        default=ACCESS_SCOPE_PAID,
        help_text="Définit si le cours est gratuit, payant ou visible dans les deux parcours."
    )

    class Meta:
        ordering = ['notion']
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

    def __str__(self):
        notion_title = getattr(self.notion, 'titre', 'Sans notion')
        return f"Cours - {notion_title}"

    @property
    def is_free_preview(self):
        return self.access_scope in {self.ACCESS_SCOPE_FREE, self.ACCESS_SCOPE_BOTH}


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
