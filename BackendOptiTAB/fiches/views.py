"""
VUES ULTRA SIMPLES pour fiches
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import FicheSynthese
from .serializers import FicheSyntheseSerializer


class FicheSyntheseViewSet(viewsets.ModelViewSet):
    queryset = FicheSynthese.objects.all()
    serializer_class = FicheSyntheseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée

    def get_queryset(self):
        queryset = super().get_queryset()
        notion = self.request.query_params.get('notion')
        
        if notion:
            queryset = queryset.filter(notion_id=notion)
            
        return queryset.filter(est_actif=True)