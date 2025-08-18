"""
VUES ULTRA SIMPLES pour cours
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Cours
from .serializers import CoursSerializer


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