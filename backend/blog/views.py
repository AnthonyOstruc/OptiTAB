"""
Vues API du blog OptiTAB
"""
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Q, Prefetch
from .models import BlogPost, BlogCategory, BlogTag, BlogNiveau, BlogContentType, BlogPostImage, BlogPostRelatedLink
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogCategorySerializer,
    BlogTagSerializer,
    BlogNiveauSerializer,
    BlogContentTypeSerializer,
    BlogPostAdminSerializer,
    BlogPostImageAdminSerializer,
    BlogPostRelatedLinkAdminSerializer,
    BlogCategoryAdminSerializer,
    BlogTagAdminSerializer,
    BlogNiveauAdminSerializer,
    BlogContentTypeAdminSerializer,
)


class BlogPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50


def _published_posts():
    return BlogPost.objects.filter(
        statut='published', est_actif=True
    ).select_related('categorie', 'niveau', 'type_contenu', 'auteur').prefetch_related(
        'tags',
        'articles_lies',
        Prefetch('liens_lies', queryset=BlogPostRelatedLink.objects.filter(est_actif=True).order_by('ordre', 'id')),
        Prefetch('images', queryset=BlogPostImage.objects.filter(est_actif=True)),
    )


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_post_list(request):
    """Liste des articles publiés avec filtres et recherche"""
    qs = _published_posts()

    # Filtre par catégorie
    categorie_slug = request.query_params.get('categorie')
    if categorie_slug:
        qs = qs.filter(categorie__slug=categorie_slug)

    # Filtre par niveau
    niveau_slug = request.query_params.get('niveau')
    if niveau_slug:
        qs = qs.filter(niveau__slug=niveau_slug)

    # Filtre par type de contenu
    type_contenu_slug = request.query_params.get('type')
    if type_contenu_slug:
        qs = qs.filter(type_contenu__slug=type_contenu_slug)

    # Filtre par tag
    tag_slug = request.query_params.get('tag')
    if tag_slug:
        qs = qs.filter(tags__slug=tag_slug)

    # Recherche texte
    search = request.query_params.get('search', '').strip()
    if search:
        qs = qs.filter(
            Q(titre__icontains=search) |
            Q(extrait__icontains=search) |
            Q(contenu__icontains=search)
        )

    qs = qs.order_by('-date_publication')

    paginator = BlogPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = BlogPostListSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_post_detail(request, slug):
    """Détail d'un article par slug"""
    try:
        post = _published_posts().get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Article non trouvé.'}, status=404)

    serializer = BlogPostDetailSerializer(post, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_category_list(request):
    """Liste des catégories actives"""
    categories = BlogCategory.objects.filter(est_actif=True).order_by('ordre', 'nom')
    serializer = BlogCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_tag_list(request):
    """Liste des tags actifs"""
    tags = BlogTag.objects.filter(est_actif=True).order_by('nom')
    serializer = BlogTagSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_niveau_list(request):
    """Liste des niveaux actifs"""
    niveaux = BlogNiveau.objects.filter(est_actif=True).order_by('ordre', 'nom')
    serializer = BlogNiveauSerializer(niveaux, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_content_type_list(request):
    """Liste des types de contenu actifs"""
    content_types = BlogContentType.objects.filter(est_actif=True).order_by('ordre', 'nom')
    serializer = BlogContentTypeSerializer(content_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_category_detail(request, slug):
    """Détail d'une catégorie par slug (pour SEO frontend)"""
    try:
        category = BlogCategory.objects.get(slug=slug, est_actif=True)
    except BlogCategory.DoesNotExist:
        return Response({'detail': 'Catégorie non trouvée.'}, status=404)
    serializer = BlogCategorySerializer(category)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_tag_detail(request, slug):
    """Détail d'un tag par slug (pour SEO frontend)"""
    try:
        tag = BlogTag.objects.get(slug=slug, est_actif=True)
    except BlogTag.DoesNotExist:
        return Response({'detail': 'Tag non trouvé.'}, status=404)
    serializer = BlogTagSerializer(tag)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def blog_sitemap(request):
    """Données sitemap pour les articles publiés et indexables"""
    posts = _published_posts().filter(
        Q(meta_robots='index') | Q(meta_robots='')
    ).order_by('-date_publication').values(
        'slug', 'date_modification', 'date_publication'
    )
    items = []
    for post in posts:
        items.append({
            'loc': f'/blog/{post["slug"]}',
            'lastmod': (post['date_modification'] or post['date_publication']).isoformat(),
            'changefreq': 'weekly',
            'priority': 0.7,
        })
    # Ajouter les catégories indexables
    categories = BlogCategory.objects.filter(
        est_actif=True
    ).exclude(meta_robots='noindex').values('slug', 'date_modification')
    for cat in categories:
        items.append({
            'loc': f'/blog/categorie/{cat["slug"]}',
            'lastmod': cat['date_modification'].isoformat() if cat['date_modification'] else None,
            'changefreq': 'weekly',
            'priority': 0.5,
        })
    return Response(items)


# ── Admin CRUD endpoints ───────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_post_list(request):
    """Liste admin de TOUS les articles (brouillons inclus)"""
    qs = BlogPost.objects.select_related(
        'categorie', 'niveau', 'type_contenu', 'auteur'
    ).prefetch_related(
        'tags', 'images', 'articles_lies', 'liens_lies'
    ).order_by('-date_creation')
    serializer = BlogPostAdminSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


def _request_list(request, key):
    if hasattr(request.data, 'getlist'):
        return [value for value in request.data.getlist(key) if str(value).strip()]

    value = request.data.get(key, [])
    if value in (None, ''):
        return []
    if isinstance(value, (list, tuple)):
        return [item for item in value if str(item).strip()]
    return [value]


def _sync_post_relations_from_request(post, request):
    if 'tags_ids_present' in request.data or 'tags_ids' in request.data:
        post.tags.set(_request_list(request, 'tags_ids'))

    if 'articles_lies_ids_present' in request.data or 'articles_lies_ids' in request.data:
        related_ids = [
            value for value in _request_list(request, 'articles_lies_ids')
            if str(value) != str(post.pk)
        ]
        post.articles_lies.set(related_ids)


def _is_truthy_request_value(value):
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}


def _clear_post_cover_if_requested(post, request):
    if request.FILES.get('image_couverture'):
        return
    if not _is_truthy_request_value(request.data.get('clear_image_couverture')):
        return
    if post.image_couverture:
        post.image_couverture.delete(save=False)
    post.image_couverture = None
    post.save(update_fields=['image_couverture', 'date_modification'])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_post_create(request):
    """Créer un article"""
    serializer = BlogPostAdminSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save(auteur=request.user)
        _sync_post_relations_from_request(post, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_post_update(request, pk):
    """Modifier un article"""
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Article non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogPostAdminSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        post = serializer.save()
        _clear_post_cover_if_requested(post, request)
        _sync_post_relations_from_request(post, request)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_post_delete(request, pk):
    """Supprimer un article"""
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Article non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ── Admin catégories ───────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_post_images(request, pk):
    """Lister ou ajouter les images inserees dans un article"""
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Article non trouve.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogPostImageAdminSerializer(
            post.images.all(),
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    if not request.FILES.get('image') and not request.data.get('image'):
        return Response({'image': ['Image obligatoire.']}, status=status.HTTP_400_BAD_REQUEST)

    serializer = BlogPostImageAdminSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_post_image_detail(request, pk, image_pk):
    """Modifier ou supprimer une image inseree dans un article"""
    try:
        image = BlogPostImage.objects.get(pk=image_pk, post_id=pk)
    except BlogPostImage.DoesNotExist:
        return Response({'detail': 'Image non trouvee.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = BlogPostImageAdminSerializer(
        image,
        data=request.data,
        partial=True,
        context={'request': request},
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_post_related_links(request, pk):
    """Lister ou ajouter les liens recommandes d'un article"""
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Article non trouve.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogPostRelatedLinkAdminSerializer(post.liens_lies.all(), many=True)
        return Response(serializer.data)

    serializer = BlogPostRelatedLinkAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_post_related_link_detail(request, pk, link_pk):
    """Modifier ou supprimer un lien recommande"""
    try:
        link = BlogPostRelatedLink.objects.get(pk=link_pk, post_id=pk)
    except BlogPostRelatedLink.DoesNotExist:
        return Response({'detail': 'Lien non trouve.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = BlogPostRelatedLinkAdminSerializer(link, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_category_list(request):
    qs = BlogCategory.objects.order_by('ordre', 'nom')
    serializer = BlogCategoryAdminSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_category_create(request):
    serializer = BlogCategoryAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_category_update(request, pk):
    try:
        cat = BlogCategory.objects.get(pk=pk)
    except BlogCategory.DoesNotExist:
        return Response({'detail': 'Catégorie non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogCategoryAdminSerializer(cat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_category_delete(request, pk):
    try:
        cat = BlogCategory.objects.get(pk=pk)
    except BlogCategory.DoesNotExist:
        return Response({'detail': 'Catégorie non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
    cat.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ── Admin tags ─────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_tag_list(request):
    qs = BlogTag.objects.order_by('nom')
    serializer = BlogTagAdminSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_tag_create(request):
    serializer = BlogTagAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_tag_update(request, pk):
    try:
        tag = BlogTag.objects.get(pk=pk)
    except BlogTag.DoesNotExist:
        return Response({'detail': 'Tag non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogTagAdminSerializer(tag, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_tag_delete(request, pk):
    try:
        tag = BlogTag.objects.get(pk=pk)
    except BlogTag.DoesNotExist:
        return Response({'detail': 'Tag non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    tag.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# —— Admin niveaux ——————————————————————————————————————————————————————————

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_niveau_list(request):
    qs = BlogNiveau.objects.order_by('ordre', 'nom')
    serializer = BlogNiveauAdminSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_niveau_create(request):
    serializer = BlogNiveauAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_niveau_update(request, pk):
    try:
        niveau = BlogNiveau.objects.get(pk=pk)
    except BlogNiveau.DoesNotExist:
        return Response({'detail': 'Niveau non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogNiveauAdminSerializer(niveau, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_niveau_delete(request, pk):
    try:
        niveau = BlogNiveau.objects.get(pk=pk)
    except BlogNiveau.DoesNotExist:
        return Response({'detail': 'Niveau non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    niveau.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# —— Admin types de contenu ——————————————————————————————————————————————

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_content_type_list(request):
    qs = BlogContentType.objects.order_by('ordre', 'nom')
    serializer = BlogContentTypeAdminSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_content_type_create(request):
    serializer = BlogContentTypeAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_content_type_update(request, pk):
    try:
        content_type = BlogContentType.objects.get(pk=pk)
    except BlogContentType.DoesNotExist:
        return Response({'detail': 'Type de contenu non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogContentTypeAdminSerializer(content_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_content_type_delete(request, pk):
    try:
        content_type = BlogContentType.objects.get(pk=pk)
    except BlogContentType.DoesNotExist:
        return Response({'detail': 'Type de contenu non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    content_type.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
