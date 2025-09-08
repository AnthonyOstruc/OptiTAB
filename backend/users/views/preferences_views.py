from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction, models
from django.shortcuts import get_object_or_404

from ..models import UserFavoriteMatiere, UserSelectedMatiere
from ..serializers.preferences_serializers import (
    UserFavoriteMatiereSerializer,
    UserSelectedMatiereSerializer,
    UserPreferencesSerializer,
    BulkUpdateMatierePreferencesSerializer
)


class UserFavoriteMatiereListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer les matières favorites de l'utilisateur"""
    serializer_class = UserFavoriteMatiereSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFavoriteMatiere.objects.filter(user=self.request.user)


class UserFavoriteMatiereDetailView(generics.RetrieveDestroyAPIView):
    """Vue pour récupérer et supprimer une matière favorite spécifique"""
    serializer_class = UserFavoriteMatiereSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFavoriteMatiere.objects.filter(user=self.request.user)


class UserSelectedMatiereListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer les onglets sélectionnés de l'utilisateur"""
    serializer_class = UserSelectedMatiereSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSelectedMatiere.objects.filter(user=self.request.user)


class UserSelectedMatiereDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour récupérer, modifier et supprimer un onglet sélectionné spécifique"""
    serializer_class = UserSelectedMatiereSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSelectedMatiere.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_preferences(request):
    """Récupérer toutes les préférences utilisateur en une seule requête"""
    try:
        user = request.user
        serializer = UserPreferencesSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la récupération des préférences : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_update_preferences(request):
    """Mettre à jour en masse les préférences de matières de l'utilisateur"""
    serializer = BulkUpdateMatierePreferencesSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            user = request.user
            
            # Mettre à jour les matières favorites
            if 'favorite_matiere_ids' in serializer.validated_data:
                favorite_ids = serializer.validated_data['favorite_matiere_ids']
                
                # Supprimer les anciennes préférences
                UserFavoriteMatiere.objects.filter(user=user).delete()
                
                # Créer les nouvelles
                if favorite_ids:
                    favorites_to_create = [
                        UserFavoriteMatiere(user=user, matiere_id=matiere_id)
                        for matiere_id in favorite_ids
                    ]
                    UserFavoriteMatiere.objects.bulk_create(favorites_to_create)
            
            # Mettre à jour les onglets sélectionnés
            if 'selected_matieres' in serializer.validated_data:
                selected_data = serializer.validated_data['selected_matieres']
                
                # Supprimer les anciens onglets
                UserSelectedMatiere.objects.filter(user=user).delete()
                
                # Créer les nouveaux
                if selected_data:
                    selected_to_create = [
                        UserSelectedMatiere(
                            user=user,
                            matiere_id=item['matiere_id'],
                            order=item['order'],
                            is_active=item.get('is_active', False)
                        )
                        for item in selected_data
                    ]
                    UserSelectedMatiere.objects.bulk_create(selected_to_create)
            
            # Mettre à jour la matière active
            if 'active_matiere_id' in serializer.validated_data:
                active_id = serializer.validated_data['active_matiere_id']
                
                # Désactiver tous les onglets
                UserSelectedMatiere.objects.filter(user=user).update(is_active=False)
                
                # Activer l'onglet spécifié
                if active_id:
                    UserSelectedMatiere.objects.filter(
                        user=user, 
                        matiere_id=active_id
                    ).update(is_active=True)
        
        # Retourner les nouvelles préférences
        user_serializer = UserPreferencesSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la mise à jour : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_matiere(request, matiere_id):
    """Ajouter une matière aux favoris"""
    try:
        user = request.user
        
        # Vérifier si pas déjà en favori
        if UserFavoriteMatiere.objects.filter(user=user, matiere_id=matiere_id).exists():
            return Response(
                {'message': 'Cette matière est déjà dans vos favoris'},
                status=status.HTTP_200_OK
            )
        
        # Créer le favori
        favorite = UserFavoriteMatiere.objects.create(user=user, matiere_id=matiere_id)
        serializer = UserFavoriteMatiereSerializer(favorite)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'ajout aux favoris : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite_matiere(request, matiere_id):
    """Supprimer une matière des favoris"""
    try:
        user = request.user
        favorite = get_object_or_404(UserFavoriteMatiere, user=user, matiere_id=matiere_id)
        favorite.delete()
        
        return Response(
            {'message': 'Matière supprimée des favoris'},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la suppression des favoris : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_selected_matiere(request, matiere_id):
    """Ajouter une matière aux onglets sélectionnés"""
    try:
        user = request.user
        
        # Vérifier si pas déjà sélectionné
        if UserSelectedMatiere.objects.filter(user=user, matiere_id=matiere_id).exists():
            return Response(
                {'message': 'Cette matière est déjà dans vos onglets'},
                status=status.HTTP_200_OK
            )
        
        # Calculer le prochain ordre
        max_order = UserSelectedMatiere.objects.filter(user=user).aggregate(
            max_order=models.Max('order')
        )['max_order'] or -1
        
        # Créer l'onglet
        selected = UserSelectedMatiere.objects.create(
            user=user, 
            matiere_id=matiere_id,
            order=max_order + 1
        )
        serializer = UserSelectedMatiereSerializer(selected)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'ajout de l\'onglet : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_selected_matiere(request, matiere_id):
    """Supprimer une matière des onglets sélectionnés"""
    try:
        user = request.user
        selected = get_object_or_404(UserSelectedMatiere, user=user, matiere_id=matiere_id)
        selected.delete()
        
        return Response(
            {'message': 'Onglet supprimé'},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la suppression de l\'onglet : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_active_matiere(request, matiere_id):
    """Définir une matière comme active"""
    try:
        user = request.user
        
        # Désactiver tous les autres onglets
        UserSelectedMatiere.objects.filter(user=user).update(is_active=False)
        
        # Activer l'onglet spécifié (ou créer s'il n'existe pas)
        selected, created = UserSelectedMatiere.objects.get_or_create(
            user=user,
            matiere_id=matiere_id,
            defaults={
                'is_active': True,
                'order': UserSelectedMatiere.objects.filter(user=user).count()
            }
        )
        
        if not created:
            selected.is_active = True
            selected.save()
        
        serializer = UserSelectedMatiereSerializer(selected)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l\'activation : {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 