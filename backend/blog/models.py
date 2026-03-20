"""
Modèles du blog OptiTAB
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from core.models import BaseModel


class BlogCategory(BaseModel):
    """Catégorie d'articles de blog"""
    nom = models.CharField(max_length=120, verbose_name="Nom")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, default="", verbose_name="Description")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    meta_description = models.CharField(max_length=160, blank=True, default="", verbose_name="Meta description")
    meta_robots = models.CharField(
        max_length=50, blank=True, default='index',
        choices=[('index', 'index, follow'), ('noindex', 'noindex, follow')],
        verbose_name="Meta robots"
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class BlogTag(BaseModel):
    """Tag pour les articles de blog"""
    nom = models.CharField(max_length=80, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    meta_description = models.CharField(max_length=160, blank=True, default="", verbose_name="Meta description")
    meta_robots = models.CharField(
        max_length=50, blank=True, default='index',
        choices=[('index', 'index, follow'), ('noindex', 'noindex, follow')],
        verbose_name="Meta robots"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class BlogPost(BaseModel):
    """Article de blog"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    ]

    # Contenu principal
    titre = models.CharField(max_length=250, verbose_name="Titre")
    slug = models.SlugField(max_length=280, unique=True, verbose_name="Slug URL")
    extrait = models.CharField(max_length=400, blank=True, default="", verbose_name="Extrait court")
    contenu = models.TextField(verbose_name="Contenu (Markdown)")
    image_couverture = models.ImageField(
        upload_to='blog/covers/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Image de couverture"
    )

    # Organisation
    categorie = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name="Catégorie"
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='articles', verbose_name="Tags")
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_articles',
        verbose_name="Auteur"
    )

    # Publication
    statut = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    date_publication = models.DateTimeField(null=True, blank=True, verbose_name="Date de publication")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    # SEO
    seo_title = models.CharField(max_length=70, blank=True, default="", verbose_name="Titre SEO")
    meta_description = models.CharField(max_length=160, blank=True, default="", verbose_name="Meta description")
    og_title = models.CharField(max_length=100, blank=True, default="", verbose_name="OG Title")
    og_description = models.CharField(max_length=200, blank=True, default="", verbose_name="OG Description")
    og_image = models.ImageField(
        upload_to='blog/og/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Image OG (Open Graph)"
    )
    alt_text_image = models.CharField(max_length=250, blank=True, default="", verbose_name="Alt text image couverture")
    meta_robots = models.CharField(
        max_length=50, blank=True, default='index',
        choices=[('index', 'index, follow'), ('noindex', 'noindex, follow')],
        verbose_name="Meta robots"
    )

    # Articles liés
    articles_lies = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        verbose_name="Articles liés"
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication', '-date_creation']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        # Auto-set publication date
        if self.statut == 'published' and not self.date_publication:
            self.date_publication = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.statut == 'published' and self.est_actif

    @property
    def reading_time(self):
        """Temps de lecture estimé en minutes"""
        word_count = len(self.contenu.split())
        return max(1, round(word_count / 200))
