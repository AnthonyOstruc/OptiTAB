"""
COURS - ULTRA SIMPLE
Chaque chapitre a son cours.
"""
from django.db import models
from django.db.models import Max, Q

from core.models import BaseEducational
from .utils import resolve_course_image_alt, resolve_course_image_title, resolve_course_title


class Cours(BaseEducational):
    """Un cours pour une notion."""

    ACCESS_SCOPE_PAID = "paid"
    ACCESS_SCOPE_FREE = "free"
    ACCESS_SCOPE_BOTH = "both"
    ACCESS_SCOPE_CHOICES = [
        (ACCESS_SCOPE_PAID, "Abonnes uniquement"),
        (ACCESS_SCOPE_FREE, "Gratuit (decouverte)"),
        (ACCESS_SCOPE_BOTH, "Gratuit + Abonnes"),
    ]

    notion = models.OneToOneField(
        "curriculum.Notion",
        on_delete=models.CASCADE,
        related_name="cours",
        null=True,  # Temporaire pour migration
    )
    video_url = models.URLField(blank=True, null=True)
    # PDF optionnel associe au cours (uploade manuellement via l'admin)
    pdf_file = models.FileField(upload_to="cours_pdfs/", blank=True, null=True)
    access_scope = models.CharField(
        max_length=10,
        choices=ACCESS_SCOPE_CHOICES,
        default=ACCESS_SCOPE_PAID,
        help_text="Definit si le cours est gratuit, payant ou visible dans les deux parcours.",
    )

    class Meta:
        ordering = ["notion"]
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

    def __str__(self):
        notion_title = getattr(self.notion, "titre", "Sans notion")
        return f"Cours - {notion_title}"

    @property
    def is_free_preview(self):
        return self.access_scope in {self.ACCESS_SCOPE_FREE, self.ACCESS_SCOPE_BOTH}


class CoursImage(models.Model):
    """Image associee a un cours."""

    TYPE_CHOICES = [
        ("illustration", "Illustration"),
    ]

    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cours_images/")
    image_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="illustration")
    position = models.PositiveIntegerField(null=True, blank=True)
    legende = models.CharField(max_length=255, null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")
    title_text = models.CharField(max_length=255, blank=True, default="")
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["cours", "position", "id"]
        verbose_name = "Image de cours"
        verbose_name_plural = "Images de cours"
        indexes = [
            models.Index(fields=["cours", "position"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["cours", "position"],
                condition=Q(position__isnull=False),
                name="unique_coursimage_position_per_cours",
            ),
        ]

    def __str__(self):
        return f"Image {self.id} - Cours {self.cours_id}"

    def save(self, *args, **kwargs):
        if self.cours_id and (self.position is None or self.position < 1):
            max_position = (
                type(self).objects
                .filter(cours_id=self.cours_id)
                .exclude(pk=self.pk)
                .aggregate(max_position=Max("position"))
                .get("max_position")
            ) or 0
            self.position = max_position + 1

        if getattr(self, "image", None):
            try:
                if not self.width:
                    self.width = int(getattr(self.image, "width", 0) or 0) or None
                if not self.height:
                    self.height = int(getattr(self.image, "height", 0) or 0) or None
            except Exception:
                pass

        super().save(*args, **kwargs)

    @property
    def resolved_alt_text(self):
        return resolve_course_image_alt(self, course_title=resolve_course_title(getattr(self, "cours", None)))

    @property
    def resolved_title_text(self):
        return resolve_course_image_title(self)
