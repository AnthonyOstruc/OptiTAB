from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from subscriptions.permissions import HasActiveSubscriptionOrPass
from .models import SynthesisSheet, SynthesisImage
from .serializers import (
    SynthesisSheetSerializer,
    SynthesisSheetCreateSerializer,
    SynthesisSheetListSerializer,
    SynthesisImageSerializer,
)


class SynthesisSheetViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des fiches de synthèse.
    - Lecture (list/retrieve) accessible aux utilisateurs authentifiés
    - Écriture (create/update/delete/duplicate/preview_data) réservée aux administrateurs
    """
    queryset = SynthesisSheet.objects.all()

    def get_permissions(self):
        # Autoriser tous les utilisateurs authentifiés à lire
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), HasActiveSubscriptionOrPass()]
        # Toutes les autres actions (écriture) sont réservées aux admins
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "duplicate",
            "preview_data",
        ]:
            return [IsAdminUser()]
        return super().get_permissions()
    
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
        ).order_by('notion', 'titre', 'id')
        
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
        if user.is_authenticated and not (user.is_staff or user.is_superuser):
            if hasattr(user, 'pays') and hasattr(user, 'niveau_pays'):
                if user.pays and user.niveau_pays:
                    # Filtrer par les contextes correspondant au pays/niveau de l'utilisateur
                    queryset = queryset.filter(
                        notion__theme__contexte__niveau__pays=user.pays,
                        notion__theme__contexte__niveau=user.niveau_pays
                    )

        # Filtrage par scope d'accès (utile côté admin)
        access_scope = self.request.query_params.get('access_scope')
        if access_scope:
            queryset = queryset.filter(access_scope=access_scope)
        
        # Recherche textuelle
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(titre__icontains=search) | 
                Q(summary__icontains=search) |
                Q(notion__titre__icontains=search)
            )
        
        return queryset

    def list(self, request, *args, **kwargs):
        """Pagination simple via ?limit=5&offset=0 pour l'admin."""
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
            page_qs = queryset[offset_value:offset_value + limit_value]
            serializer = self.get_serializer(page_qs, many=True)
            return Response({
                'count': total,
                'limit': limit_value,
                'offset': offset_value,
                'results': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        """Uploader une image pour une fiche de synthèse"""
        sheet = self.get_object()
        image_file = request.FILES.get('image')
        image_type = request.data.get('image_type', 'illustration')
        position = request.data.get('position')
        caption = request.data.get('caption')

        if not image_file:
            return Response({'detail': 'Image manquante'}, status=status.HTTP_400_BAD_REQUEST)

        img = SynthesisImage.objects.create(
            sheet=sheet,
            image=image_file,
            image_type=image_type,
            position=position,
            caption=caption,
        )

        return Response({'id': img.id, 'image': request.build_absolute_uri(img.image.url) if hasattr(img.image, 'url') else ''}, status=status.HTTP_201_CREATED)
    
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
            'reading_time_minutes': original.reading_time_minutes,
            'access_scope': original.access_scope,
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


class SynthesisImageViewSet(viewsets.ModelViewSet):
    """CRUD pour les images des fiches de synthèse.

    Endpoint attendu par le frontend: /api/sheet-images/?sheet=<id>
    Autorise lecture publique; écriture pour utilisateurs authentifiés.
    """
    queryset = SynthesisImage.objects.all()
    serializer_class = SynthesisImageSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Lecture: utilisateurs authentifiés
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), HasActiveSubscriptionOrPass()]
        # Écriture réservée aux admins
        return [IsAdminUser()]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def get_queryset(self):
        queryset = super().get_queryset()
        sheet_id = self.request.query_params.get('sheet')
        if sheet_id:
            queryset = queryset.filter(sheet_id=sheet_id)
        return queryset.order_by('position', 'id')
