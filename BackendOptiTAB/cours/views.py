"""
VUES ULTRA SIMPLES pour cours
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Cours, CoursImage
from .serializers import CoursSerializer, CoursImageSerializer


class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée

    def get_queryset(self):
        queryset = super().get_queryset()
        chapitre = self.request.query_params.get('chapitre')
        
        if chapitre:
            queryset = queryset.filter(chapitre_id=chapitre)
            
        return queryset.filter(est_actif=True)


class CoursImageViewSet(viewsets.ModelViewSet):
    """CRUD pour les images de cours

    Frontend attend /api/cours/cours-images/ avec filtre ?cours=<id>
    """
    queryset = CoursImage.objects.all()
    serializer_class = CoursImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        cours_id = self.request.query_params.get('cours')
        if cours_id:
            queryset = queryset.filter(cours_id=cours_id)
        return queryset.order_by('position', 'id')