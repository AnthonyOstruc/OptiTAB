from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from core.views import AdminRequiredMixin
from .models import SynthesisSheet
from .serializers import (
    SynthesisSheetSerializer, 
    SynthesisSheetCreateSerializer,
    SynthesisSheetListSerializer
)


class SynthesisSheetViewSet(AdminRequiredMixin, viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des fiches de synthèse
    Réservé aux administrateurs
    """
    queryset = SynthesisSheet.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SynthesisSheetListSerializer
        elif self.action == 'create':
            return SynthesisSheetCreateSerializer
        return SynthesisSheetSerializer
    
    def get_queryset(self):
        queryset = SynthesisSheet.objects.select_related(
            'notion',
            'notion__theme',
            'notion__theme__matiere'
        ).order_by('notion', 'ordre', 'titre')
        
        # Filtrage par notion
        notion_id = self.request.query_params.get('notion', None)
        if notion_id:
            queryset = queryset.filter(notion_id=notion_id)
        
        # Filtrage par matière
        matiere_id = self.request.query_params.get('matiere', None)
        if matiere_id:
            queryset = queryset.filter(notion__theme__matiere_id=matiere_id)
        
        # Filtrage par contexte utilisateur (pays/niveau) si l'utilisateur est connecté
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'pays') and hasattr(user, 'niveau_pays'):
            if user.pays and user.niveau_pays:
                # Filtrer par les contextes correspondant au pays/niveau de l'utilisateur
                queryset = queryset.filter(
                    notion__theme__contexte__niveau__pays=user.pays,
                    notion__theme__contexte__niveau=user.niveau_pays
                )
        
        # Recherche textuelle
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(titre__icontains=search) | 
                Q(summary__icontains=search) |
                Q(notion__titre__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Dupliquer une fiche de synthèse"""
        original = self.get_object()
        
        # Créer une copie
        duplicate_data = {
            'titre': f"{original.titre} (Copie)",
            'notion': original.notion.id,
            'summary': original.summary,
            'key_points': original.key_points,
            'formulas': original.formulas,
            'examples': original.examples,
            'difficulty': original.difficulty,
            'ordre': original.ordre + 1,
            'reading_time_minutes': original.reading_time_minutes
        }
        
        serializer = SynthesisSheetCreateSerializer(data=duplicate_data)
        if serializer.is_valid():
            duplicate = serializer.save()
            return Response(
                SynthesisSheetSerializer(duplicate).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def preview_data(self, request):
        """Données pour la prévisualisation sans sauvegarder"""
        # Récupère les données du query string pour la prévisualisation
        titre = request.query_params.get('titre', '')
        summary = request.query_params.get('summary', '')
        
        # Simule le rendu markdown (ici on retourne juste les données)
        return Response({
            'titre': titre,
            'summary': summary,
            'rendered_html': summary,  # En production, utiliser un renderer markdown
            'reading_time': len(summary.split()) // 200 if summary else 1  # Estimation
        })
