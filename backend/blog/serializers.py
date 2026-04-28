"""
Serializers du blog OptiTAB
"""
from django.utils.text import slugify
from rest_framework import serializers

from .models import BlogCategory, BlogTag, BlogNiveau, BlogContentType, BlogPost, BlogPostImage


class BlogCategorySerializer(serializers.ModelSerializer):
    articles_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = ['id', 'nom', 'slug', 'description', 'meta_description', 'meta_robots', 'articles_count']

    def get_articles_count(self, obj):
        return obj.articles.filter(statut='published', est_actif=True).count()


class BlogTagSerializer(serializers.ModelSerializer):
    articles_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogTag
        fields = ['id', 'nom', 'slug', 'meta_description', 'meta_robots', 'articles_count']

    def get_articles_count(self, obj):
        return obj.articles.filter(statut='published', est_actif=True).count()


class BlogNiveauSerializer(serializers.ModelSerializer):
    articles_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogNiveau
        fields = ['id', 'nom', 'slug', 'ordre', 'articles_count']

    def get_articles_count(self, obj):
        return obj.articles.filter(statut='published', est_actif=True).count()


class BlogContentTypeSerializer(serializers.ModelSerializer):
    articles_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogContentType
        fields = ['id', 'nom', 'slug', 'ordre', 'articles_count']

    def get_articles_count(self, obj):
        return obj.articles.filter(statut='published', est_actif=True).count()


class BlogPostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPostImage
        fields = [
            'id', 'image_url', 'position', 'align', 'width_percent',
            'alt_text', 'caption', 'title_text',
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer leger pour la liste d'articles"""

    categorie = BlogCategorySerializer(read_only=True)
    niveau = BlogNiveauSerializer(read_only=True)
    type_contenu = BlogContentTypeSerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    auteur_nom = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    image_couverture_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'titre', 'slug', 'extrait', 'image_couverture_url',
            'alt_text_image',
            'categorie', 'niveau', 'type_contenu',
            'tags', 'auteur_nom', 'statut',
            'date_publication', 'reading_time',
        ]

    def get_auteur_nom(self, obj):
        if obj.auteur:
            name = f'{obj.auteur.first_name} {obj.auteur.last_name}'.strip()
            return name or obj.auteur.email
        return 'OptiTAB'

    def get_image_couverture_url(self, obj):
        if obj.image_couverture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_couverture.url)
            return obj.image_couverture.url
        return None


class BlogPostDetailSerializer(BlogPostListSerializer):
    """Serializer complet pour le detail d'un article"""

    articles_lies = BlogPostListSerializer(many=True, read_only=True)
    og_image_url = serializers.SerializerMethodField()
    images = BlogPostImageSerializer(many=True, read_only=True)

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            'contenu', 'images', 'articles_lies',
            'seo_title', 'meta_description', 'og_title', 'og_description',
            'og_image_url', 'meta_robots',
            'date_creation', 'date_modification',
        ]

    def get_og_image_url(self, obj):
        if obj.og_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.og_image.url)
            return obj.og_image.url
        return None


class _SlugAutoUniqueMixin:
    slug_fallback = 'item'

    def _build_unique_slug(self, model, source_text, max_length):
        base = slugify((source_text or '').strip())[:max_length]
        if not base:
            base = self.slug_fallback

        qs = model.objects.all()
        if self.instance and getattr(self.instance, 'pk', None):
            qs = qs.exclude(pk=self.instance.pk)

        slug = base
        index = 2
        while qs.filter(slug=slug).exists():
            suffix = f'-{index}'
            slug = f'{base[:max_length - len(suffix)]}{suffix}'
            index += 1
        return slug

    def validate(self, attrs):
        attrs = super().validate(attrs)
        nom = (attrs.get('nom') or getattr(self.instance, 'nom', '') or '').strip()
        raw_slug = (attrs.get('slug') or '').strip()
        source = raw_slug or nom or self.slug_fallback
        max_length = getattr(self.fields.get('slug'), 'max_length', 140) or 140
        attrs['slug'] = self._build_unique_slug(self.Meta.model, source, max_length)
        return attrs


class BlogCategoryAdminSerializer(_SlugAutoUniqueMixin, serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'nom', 'slug', 'description', 'meta_description', 'meta_robots', 'ordre', 'est_actif']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True, 'validators': []},
        }


class BlogTagAdminSerializer(_SlugAutoUniqueMixin, serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['id', 'nom', 'slug', 'meta_description', 'meta_robots', 'est_actif']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True, 'validators': []},
        }


class BlogNiveauAdminSerializer(_SlugAutoUniqueMixin, serializers.ModelSerializer):
    class Meta:
        model = BlogNiveau
        fields = ['id', 'nom', 'slug', 'ordre', 'est_actif']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True, 'validators': []},
        }


class BlogContentTypeAdminSerializer(_SlugAutoUniqueMixin, serializers.ModelSerializer):
    class Meta:
        model = BlogContentType
        fields = ['id', 'nom', 'slug', 'ordre', 'est_actif']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True, 'validators': []},
        }


class BlogPostAdminSerializer(serializers.ModelSerializer):
    """Serializer admin pour la liste et le CRUD des articles"""

    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True, default='')
    auteur_nom = serializers.SerializerMethodField()
    niveau_nom = serializers.CharField(source='niveau.nom', read_only=True, default='')
    type_contenu_nom = serializers.CharField(source='type_contenu.nom', read_only=True, default='')

    tags_ids = serializers.PrimaryKeyRelatedField(
        source='tags', many=True, queryset=BlogTag.objects.all(), required=False,
    )
    articles_lies_ids = serializers.PrimaryKeyRelatedField(
        source='articles_lies', many=True, queryset=BlogPost.objects.all(), required=False,
    )

    image_couverture_url = serializers.SerializerMethodField()
    og_image_url = serializers.SerializerMethodField()
    images = BlogPostImageSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'titre', 'slug', 'extrait', 'contenu',
            'images',
            'image_couverture', 'image_couverture_url',
            'og_image', 'og_image_url',
            'alt_text_image',
            'categorie', 'categorie_nom',
            'niveau', 'niveau_nom',
            'type_contenu', 'type_contenu_nom',
            'tags_ids',
            'auteur', 'auteur_nom',
            'statut', 'date_publication', 'ordre', 'est_actif',
            'seo_title', 'meta_description', 'og_title', 'og_description',
            'meta_robots',
            'articles_lies_ids',
            'date_creation', 'date_modification',
        ]
        read_only_fields = ['date_creation', 'date_modification']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True, 'validators': []},
            'categorie': {'required': False, 'allow_null': True},
            'niveau': {'required': False, 'allow_null': True},
            'type_contenu': {'required': False, 'allow_null': True},
            'est_actif': {'required': False, 'default': True},
        }

    def _build_unique_slug(self, source_text, max_length=280):
        base = slugify((source_text or '').strip())[:max_length]
        if not base:
            base = 'article'

        qs = BlogPost.objects.all()
        if self.instance and getattr(self.instance, 'pk', None):
            qs = qs.exclude(pk=self.instance.pk)

        slug = base
        index = 2
        while qs.filter(slug=slug).exists():
            suffix = f'-{index}'
            slug = f'{base[:max_length - len(suffix)]}{suffix}'
            index += 1
        return slug

    def validate(self, attrs):
        attrs = super().validate(attrs)
        titre = (attrs.get('titre') or getattr(self.instance, 'titre', '') or '').strip()
        raw_slug = (attrs.get('slug') or '').strip()
        attrs['slug'] = self._build_unique_slug(raw_slug or titre)
        return attrs

    def get_image_couverture_url(self, obj):
        if obj.image_couverture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_couverture.url)
            return obj.image_couverture.url
        return None

    def get_og_image_url(self, obj):
        if obj.og_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.og_image.url)
            return obj.og_image.url
        return None

    def get_auteur_nom(self, obj):
        if obj.auteur:
            name = f'{obj.auteur.first_name} {obj.auteur.last_name}'.strip()
            return name or obj.auteur.email
        return ''


class BlogPostImageAdminSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPostImage
        fields = [
            'id', 'post', 'image', 'image_url', 'position', 'align',
            'width_percent', 'alt_text', 'caption', 'title_text',
            'est_actif', 'date_creation', 'date_modification',
        ]
        read_only_fields = ['post', 'image_url', 'date_creation', 'date_modification']
        extra_kwargs = {
            'image': {'required': False},
            'align': {'required': False},
            'width_percent': {'required': False},
            'position': {'required': False},
            'est_actif': {'required': False},
        }

    def validate_width_percent(self, value):
        value = int(value or 100)
        if value < 20 or value > 100:
            raise serializers.ValidationError('La largeur doit etre comprise entre 20 et 100%.')
        return value

    def validate_position(self, value):
        value = int(value or 1)
        if value < 1:
            raise serializers.ValidationError('La position doit etre superieure ou egale a 1.')
        return value

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
