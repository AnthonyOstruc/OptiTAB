"""
Serializers du blog OptiTAB
"""
from rest_framework import serializers
from .models import BlogCategory, BlogTag, BlogPost


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


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer léger pour la liste d'articles"""
    categorie = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    auteur_nom = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    image_couverture_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'titre', 'slug', 'extrait', 'image_couverture_url',
            'alt_text_image',
            'categorie', 'tags', 'auteur_nom', 'statut',
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
    """Serializer complet pour le détail d'un article"""
    articles_lies = BlogPostListSerializer(many=True, read_only=True)
    og_image_url = serializers.SerializerMethodField()

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            'contenu', 'articles_lies',
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


# ── Admin serializers ──────────────────────────────────────────────

class BlogCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'nom', 'slug', 'description', 'meta_description', 'meta_robots', 'ordre', 'est_actif']


class BlogTagAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['id', 'nom', 'slug', 'meta_description', 'meta_robots', 'est_actif']


class BlogPostAdminSerializer(serializers.ModelSerializer):
    """Serializer admin pour la liste et le CRUD des articles"""
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True, default='')
    auteur_nom = serializers.SerializerMethodField()
    tags_ids = serializers.PrimaryKeyRelatedField(
        source='tags', many=True, queryset=BlogTag.objects.all(), required=False,
    )
    articles_lies_ids = serializers.PrimaryKeyRelatedField(
        source='articles_lies', many=True, queryset=BlogPost.objects.all(), required=False,
    )

    image_couverture_url = serializers.SerializerMethodField()
    og_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'titre', 'slug', 'extrait', 'contenu',
            'image_couverture', 'image_couverture_url',
            'og_image', 'og_image_url',
            'alt_text_image',
            'categorie', 'categorie_nom',
            'tags_ids',
            'auteur', 'auteur_nom',
            'statut', 'date_publication', 'ordre', 'est_actif',
            'seo_title', 'meta_description', 'og_title', 'og_description',
            'meta_robots',
            'articles_lies_ids',
            'date_creation', 'date_modification',
        ]
        read_only_fields = ['date_creation', 'date_modification']

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
