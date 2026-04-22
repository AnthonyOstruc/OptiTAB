"""
Vues API du blog OptiTAB
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Q
from .models import BlogPost, BlogCategory, BlogTag, BlogNiveau, BlogContentType
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogCategorySerializer,
    BlogTagSerializer,
    BlogNiveauSerializer,
    BlogContentTypeSerializer,
    BlogPostAdminSerializer,
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
    ).select_related('categorie', 'niveau', 'type_contenu', 'auteur').prefetch_related('tags')


@api_view(['GET'])
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
@permission_classes([AllowAny])
def blog_post_detail(request, slug):
    """Détail d'un article par slug"""
    try:
        post = _published_posts().prefetch_related('articles_lies').get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Article non trouvé.'}, status=404)

    serializer = BlogPostDetailSerializer(post, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def blog_category_list(request):
    """Liste des catégories actives"""
    categories = BlogCategory.objects.filter(est_actif=True).order_by('ordre', 'nom')
    serializer = BlogCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def blog_tag_list(request):
    """Liste des tags actifs"""
    tags = BlogTag.objects.filter(est_actif=True).order_by('nom')
    serializer = BlogTagSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def blog_niveau_list(request):
    """Liste des niveaux actifs"""
    niveaux = BlogNiveau.objects.filter(est_actif=True).order_by('ordre', 'nom')
    serializer = BlogNiveauSerializer(niveaux, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def blog_content_type_list(request):
    """Liste des types de contenu actifs"""
    content_types = BlogContentType.objects.filter(est_actif=True).order_by('ordre', 'nom')
    serializer = BlogContentTypeSerializer(content_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
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
    qs = BlogPost.objects.select_related('categorie', 'niveau', 'type_contenu', 'auteur').prefetch_related('tags').order_by('-date_creation')
    serializer = BlogPostAdminSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_post_create(request):
    """Créer un article"""
    serializer = BlogPostAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(auteur=request.user)
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
        serializer.save()
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
