"""
SYNTHESIS SHEETS - Fiches de synthèse
Fiches de résumé par chapitre pour faciliter les révisions
"""
from django.db import models
from core.models import BaseContent


class SynthesisSheet(BaseContent):
    """Une fiche de synthèse pour une notion"""

    SHEET_TYPE_SUMMARY = 'summary'
    SHEET_TYPE_TABLE = 'table'
    SHEET_TYPE_CHOICES = [
        (SHEET_TYPE_SUMMARY, 'Fiche de synthèse'),
        (SHEET_TYPE_TABLE, 'Tableau & Formules'),
    ]

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
        verbose_name='Résumé',
        help_text='Contenu principal de la fiche en Markdown'
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
        verbose_name='Difficulté'
    )

    # Points clés (optionnel, en JSON)
    key_points = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Points clés',
        help_text='Liste des points essentiels à retenir'
    )

    # Formules importantes (optionnel, en JSON)
    formulas = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Formules',
        help_text='Formules mathématiques importantes'
    )

    # Exemples (optionnel, en JSON)
    examples = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Exemples',
        help_text="Exemples concrets d'application"
    )

    # Durée de lecture estimée en minutes
    reading_time_minutes = models.PositiveIntegerField(
        default=5,
        verbose_name='Temps de lecture (min)'
    )

    show_on_home = models.BooleanField(
        default=False,
        verbose_name="Mettre en avant sur l'accueil",
        help_text="Active l'affichage de cette fiche sur la page d'accueil."
    )
    show_on_public_site = models.BooleanField(
        default=True,
        verbose_name='Visible sur le site public',
        help_text='Permet de masquer une fiche tout en la conservant en base.'
    )

    access_scope = models.CharField(
        max_length=10,
        choices=ACCESS_SCOPE_CHOICES,
        default=ACCESS_SCOPE_PAID,
        help_text='Définit si cette fiche est gratuite, payante ou visible dans les deux parcours.'
    )

    sheet_type = models.CharField(
        max_length=10,
        choices=SHEET_TYPE_CHOICES,
        default=SHEET_TYPE_SUMMARY,
        db_index=True,
        help_text='Définit le type de fiche (synthèse ou tableau/formules).'
    )

    class Meta:
        ordering = ['notion', 'titre']
        verbose_name = 'Fiche de synthèse'
        verbose_name_plural = 'Fiches de synthèse'
        unique_together = [['notion', 'titre', 'sheet_type']]

    def __str__(self):
        return f'Fiche - {self.notion.titre} - {self.titre}'

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
        verbose_name = 'Image de fiche de synthèse'
        verbose_name_plural = 'Images de fiches de synthèse'
        indexes = [
            models.Index(fields=['sheet', 'position']),
        ]

    def __str__(self):
        return f'Image {self.id} - Sheet {self.sheet_id}'
