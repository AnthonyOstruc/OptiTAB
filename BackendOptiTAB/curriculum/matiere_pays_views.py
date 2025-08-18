"""
Vues pour la gestion des matières par pays et utilisateur
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from curriculum.models import Matiere
from curriculum.serializers import MatiereSerializer


class MatierePaysViewSet(viewsets.ViewSet):
    """
    ViewSet pour gérer les matières selon le pays/niveau de l'utilisateur
    Compatible avec l'ancienne API frontend
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """GET /api/matiere-pays/ - Toutes les matières"""
        matieres = Matiere.objects.filter(est_actif=True).prefetch_related('niveaux', 'niveaux__pays', 'pays').order_by('ordre', 'titre')
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pour_utilisateur(self, request):
        """GET /api/matiere-pays/pour_utilisateur/ - Matières pour l'utilisateur connecté"""
        user = request.user
        
        # Vérifier si l'utilisateur a un pays et niveau configurés
        if not user.pays or not user.niveau_pays:
            return Response({
                'error': 'Utilisateur non configuré',
                'message': 'Veuillez configurer votre pays et niveau dans votre profil'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer les matières pour le pays/niveau de l'utilisateur
        matieres = Matiere.objects.filter(
            Q(pays=user.pays) | Q(niveaux__pays=user.pays),
            Q(niveaux=user.niveau_pays) | Q(pays=user.pays),
            est_actif=True
        ).distinct().order_by('ordre', 'titre')
        
        serializer = MatiereSerializer(matieres, many=True)
        
        return Response({
            'message': f'Matières pour {user.pays.nom} - {user.niveau_pays.nom}',
            'count': len(serializer.data),
            'data': serializer.data
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matiere_pays_pour_utilisateur(request):
    """
    Alternative function-based view pour /api/matiere-pays/pour_utilisateur/
    """
    user = request.user
    
    # Vérifier si l'utilisateur a un pays et niveau configurés
    if not user.pays or not user.niveau_pays:
        return Response({
            'error': 'Utilisateur non configuré',
            'message': 'Veuillez configurer votre pays et niveau dans votre profil',
            'matieres': []
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Récupérer les matières pour le pays/niveau de l'utilisateur
    matieres = Matiere.objects.filter(
        Q(pays=user.pays) | Q(niveaux__pays=user.pays),
        Q(niveaux=user.niveau_pays) | Q(pays=user.pays),
        est_actif=True
    ).distinct().order_by('ordre', 'titre')
    
    serializer = MatiereSerializer(matieres, many=True)
    
    return Response(serializer.data)
