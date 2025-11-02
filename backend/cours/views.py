"""
VUES ULTRA SIMPLES pour cours
"""
from rest_framework import viewsets
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

        if notion:
            queryset = queryset.filter(notion_id=notion)
        if matiere:
            # Joindre via Notion -> Theme -> Matiere
            queryset = queryset.select_related('notion', 'notion__theme', 'notion__theme__matiere')
            queryset = queryset.filter(notion__theme__matiere_id=matiere)

        return queryset.filter(est_actif=True)


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
