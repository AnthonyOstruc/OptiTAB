"""
VUES ULTRA SIMPLES pour cours
"""
import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated

from subscriptions.permissions import HasActiveSubscriptionOrPass
from .models import Cours, CoursImage
from .serializers import CoursSerializer, CoursImageSerializer


class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasActiveSubscriptionOrPass()]

    def get_serializer_context(self):
        # Injecter la requête pour construire des URLs absolues dans le serializer
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def get_queryset(self):
        queryset = super().get_queryset()
        # Nouveau filtrage direct par notion (suppression des chapitres)
        notion = self.request.query_params.get('notion')
        matiere = self.request.query_params.get('matiere')
        search = self.request.query_params.get('search') or self.request.query_params.get('q')

        if notion:
            queryset = queryset.filter(notion_id=notion)
        if matiere:
            # Joindre via Notion -> Theme -> Matiere
            queryset = queryset.select_related('notion', 'notion__theme', 'notion__theme__matiere')
            queryset = queryset.filter(notion__theme__matiere_id=matiere)

        if search:
            queryset = queryset.filter(titre__icontains=search)

        return queryset.filter(est_actif=True).select_related('notion', 'notion__theme', 'notion__theme__matiere').order_by('ordre', 'id')

    def list(self, request, *args, **kwargs):
        """Pagination légère pour l'admin via ?limit=5&offset=0."""
        queryset = self.filter_queryset(self.get_queryset())

        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset', 0)

        if limit is not None:
            try:
                limit_value = int(limit)
                offset_value = int(offset or 0)
                if limit_value <= 0 or offset_value < 0:
                    raise ValueError
            except ValueError:
                return Response({'detail': 'Paramètres de pagination invalides'}, status=status.HTTP_400_BAD_REQUEST)

            total = queryset.count()
            serializer = self.get_serializer(queryset[offset_value:offset_value + limit_value], many=True)
            return Response({
                'count': total,
                'limit': limit_value,
                'offset': offset_value,
                'results': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CoursImageViewSet(viewsets.ModelViewSet):
    """CRUD pour les images de cours

    Frontend attend /api/cours/cours-images/ avec filtre ?cours=<id>
    """
    queryset = CoursImage.objects.all()
    serializer_class = CoursImageSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def get_queryset(self):
        queryset = super().get_queryset()
        cours_id = self.request.query_params.get('cours')
        if cours_id:
            queryset = queryset.filter(cours_id=cours_id)
        return queryset.order_by('position', 'id')

    @action(detail=False, methods=['post'], url_path='duplicate')
    def duplicate_images(self, request, *args, **kwargs):
        source_cours_id = request.data.get('source_cours')
        target_cours_id = request.data.get('target_cours')
        replace_existing = bool(request.data.get('replace_existing'))

        if not source_cours_id or not target_cours_id:
            return Response(
                {'detail': 'source_cours et target_cours sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            source_cours = Cours.objects.get(pk=source_cours_id)
            target_cours = Cours.objects.get(pk=target_cours_id)
        except Cours.DoesNotExist:
            return Response({'detail': 'Cours introuvable'}, status=status.HTTP_404_NOT_FOUND)

        if replace_existing:
            target_cours.images.all().delete()

        duplicated = 0
        for img in source_cours.images.all().order_by('position', 'id'):
            if not img.image:
                continue
            new_image = CoursImage(
                cours=target_cours,
                image_type=img.image_type,
                position=img.position,
                legende=img.legende
            )
            try:
                with img.image.open('rb') as original_file:
                    filename = os.path.basename(img.image.name or f'cours-image-{img.id}')
                    new_image.image.save(filename, ContentFile(original_file.read()), save=False)
                new_image.save()
                duplicated += 1
            except Exception:  # pragma: no cover - ignorer les erreurs individuelles
                continue

        serializer = self.get_serializer(
            target_cours.images.all().order_by('position', 'id'),
            many=True
        )
        return Response({'duplicated': duplicated, 'images': serializer.data})
