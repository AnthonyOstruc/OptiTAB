from django.db import models
from django.utils.text import slugify
import uuid

from core.models import BaseContent


class FreeLearningResource(BaseContent):
    """
    Ressource gratuite utilisée pour teaser les abonnements.

    Peut représenter un cours, une fiche de synthèse (résumé) ou un exercice.
    """

    TYPE_COURSE = 'course'
    TYPE_EXERCISE = 'exercise'
    TYPE_SUMMARY = 'summary'

    TYPE_CHOICES = [
        (TYPE_COURSE, 'Cours'),
        (TYPE_EXERCISE, 'Exercice'),
        (TYPE_SUMMARY, 'Résumé'),
    ]

    slug = models.SlugField(max_length=255, unique=True)
    accroche = models.CharField(max_length=200, blank=True)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    niveau = models.ForeignKey(
        'pays.Niveau',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='free_resources'
    )
    matiere = models.ForeignKey(
        'curriculum.Matiere',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='free_resources'
    )
    notion = models.ForeignKey(
        'curriculum.Notion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='free_resources'
    )
    excerpt = models.TextField(blank=True)
    contenu_html = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)
    badge = models.CharField(max_length=60, blank=True)
    lecture_duree = models.CharField(max_length=60, blank=True)
    tag_secondaire = models.CharField(max_length=60, blank=True)
    est_publie = models.BooleanField(default=False)

    class Meta:
        ordering = ['resource_type', 'ordre', 'titre']
        verbose_name = "Ressource gratuite"
        verbose_name_plural = "Ressources gratuites"

    def __str__(self):
        label = dict(self.TYPE_CHOICES).get(self.resource_type, 'Ressource')
        return f"{label} gratuit - {self.titre}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre) or slugify(f"ressource-{uuid.uuid4().hex[:6]}")
            slug = base_slug
            counter = 1
            while FreeLearningResource.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def type_label(self):
        return dict(self.TYPE_CHOICES).get(self.resource_type, self.resource_type)

# Create your models here.
