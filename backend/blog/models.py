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


class BlogNiveau(BaseModel):
    """Niveau scolaire pour classer les articles"""
    nom = models.CharField(max_length=80, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class BlogContentType(BaseModel):
    """Type de contenu d'article"""
    nom = models.CharField(max_length=120, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Slug")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Type de contenu"
        verbose_name_plural = "Types de contenu"
        ordering = ['ordre', 'nom']

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
    niveau = models.ForeignKey(
        BlogNiveau,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name="Niveau",
    )
    type_contenu = models.ForeignKey(
        BlogContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name="Type de contenu",
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


class BlogPostImage(BaseModel):
    """Image inseree dans le contenu d'un article de blog"""

    ALIGN_CHOICES = [
        ('center', 'Centree'),
        ('left', 'Gauche'),
        ('right', 'Droite'),
        ('full', 'Pleine largeur'),
    ]

    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Article",
    )
    image = models.ImageField(
        upload_to='blog/content/%Y/%m/',
        verbose_name="Image",
    )
    position = models.PositiveIntegerField(default=1, verbose_name="Position")
    align = models.CharField(
        max_length=20,
        choices=ALIGN_CHOICES,
        default='center',
        verbose_name="Alignement",
    )
    width_percent = models.PositiveIntegerField(default=100, verbose_name="Largeur (%)")
    alt_text = models.CharField(max_length=250, blank=True, default="", verbose_name="Texte alternatif")
    caption = models.CharField(max_length=300, blank=True, default="", verbose_name="Legende")
    title_text = models.CharField(max_length=160, blank=True, default="", verbose_name="Titre image")

    class Meta:
        verbose_name = "Image d'article"
        verbose_name_plural = "Images d'articles"
        ordering = ['position', 'id']

    def __str__(self):
        return f'{self.post.titre} - image {self.position}'


class BlogPostRelatedLink(BaseModel):
    """Lien recommande affiche en fin d'article."""

    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='liens_lies',
        verbose_name="Article",
    )
    titre = models.CharField(max_length=220, verbose_name="Titre du lien")
    url = models.CharField(max_length=500, verbose_name="URL")
    description = models.CharField(max_length=260, blank=True, default="", verbose_name="Description")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Lien recommande"
        verbose_name_plural = "Liens recommandes"
        ordering = ['ordre', 'id']

    def __str__(self):
        return self.titre
