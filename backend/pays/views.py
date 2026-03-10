"""
VUES HIÉRARCHIQUES PROFESSIONNELLES - Architecture REST cohérente
Structure: Pays → Niveau → Matière → Thème → Notion → Chapitre → Exercice
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Pays, Niveau
from .serializers import PaysSerializer, NiveauSerializer


class PaysViewSet(viewsets.ModelViewSet):
    """ViewSet pour les pays avec actions hiérarchiques"""
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture admin
    
    def get_queryset(self):
        from django.db.models import Count
        queryset = Pays.objects.all().annotate(
            nombre_niveaux=Count('niveaux', filter=Q(niveaux__est_actif=True), distinct=True),
            nombre_utilisateurs=Count('users', distinct=True)
        )
        
        # Filtrer par statut actif
        est_actif = self.request.query_params.get('est_actif')
        if est_actif is not None:
            queryset = queryset.filter(est_actif=est_actif.lower() == 'true')
        
        # Recherche par nom ou code ISO
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) | 
                Q(code_iso__icontains=search)
            )
        
        return queryset.order_by('ordre', 'nom')
    
    @action(detail=True, methods=['get'])
    def niveaux(self, request, pk=None):
        """GET /api/pays/{id}/niveaux/ - Récupère les niveaux d'un pays"""
        pays = self.get_object()
        niveaux = Niveau.objects.filter(
            pays=pays, 
            est_actif=True
        ).order_by('ordre', 'nom')
        
        serializer = NiveauSerializer(niveaux, many=True)
        return Response(serializer.data)


class NiveauViewSet(viewsets.ModelViewSet):
    """ViewSet pour les niveaux avec actions hiérarchiques"""
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture admin
    
    def get_queryset(self):
        queryset = Niveau.objects.select_related('pays').all()
        
        # Filtrer par pays
        pays_id = self.request.query_params.get('pays_id')
        if pays_id:
            queryset = queryset.filter(pays_id=pays_id)
        
        # Filtrer par statut actif
        est_actif = self.request.query_params.get('est_actif')
        if est_actif is not None:
            queryset = queryset.filter(est_actif=est_actif.lower() == 'true')
        
        return queryset.order_by('pays', 'ordre', 'nom')

    def list(self, request, *args, **kwargs):
        # Eviter le calcul des statistiques sur la liste pour accélérer
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer_context = { 'request': request, 'include_stats': False }
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # Inclure les statistiques uniquement sur le détail
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={ 'request': request, 'include_stats': True })
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def matieres(self, request, pk=None):
        """GET /api/niveaux/{id}/matieres/ - Récupère les matières d'un niveau"""
        niveau = self.get_object()
        
        # Importer ici pour éviter les imports circulaires
        from curriculum.models import Matiere
        from curriculum.serializers import MatiereSerializer
        
        matieres = Matiere.objects.filter(
            niveau=niveau,
            est_actif=True
        ).order_by('ordre', 'titre')
        
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def demo(self, request, pk=None):
        """GET /api/niveaux/{id}/demo/ - Contenu démo gratuit (chapitre + exercices)
        
        Accessible à tout utilisateur authentifié, sans abonnement.
        Retourne la notion démo, son cours, sa synthèse et les exercices démo.
        """
        niveau = self.get_object()

        if not niveau.demo_notion_id:
            return Response({'detail': 'Aucun chapitre démo configuré pour ce niveau.'}, status=status.HTTP_404_NOT_FOUND)

        from curriculum.models import Notion, Exercice
        from curriculum.serializers import ExerciceSerializer
        from cours.models import Cours
        from cours.serializers import CoursSerializer
        from synthesis.models import SynthesisSheet

        notion = Notion.objects.select_related('theme', 'theme__matiere').get(pk=niveau.demo_notion_id)
        
        # Cours lié à la notion (OneToOne)
        cours_data = None
        try:
            cours = Cours.objects.prefetch_related('images').get(notion=notion, est_actif=True)
            cours_data = CoursSerializer(cours, context={'request': request}).data
        except Cours.DoesNotExist:
            pass

        # Synthèse liée à la notion
        synthese_data = None
        try:
            synthese = SynthesisSheet.objects.get(notion=notion, est_actif=True)
            synthese_data = {'id': synthese.id, 'titre': synthese.titre, 'summary': synthese.summary}
        except Exception:
            pass

        # Exercices démo choisis par l'admin
        demo_exercice_ids = list(niveau.demo_exercices.values_list('id', flat=True))
        exercices = Exercice.objects.filter(id__in=demo_exercice_ids, est_actif=True).prefetch_related('images')
        exercices_data = ExerciceSerializer(exercices, many=True, context={'request': request}).data

        return Response({
            'notion': {
                'id': notion.id,
                'titre': notion.titre,
                'theme': notion.theme.titre if notion.theme else None,
                'matiere': notion.theme.matiere.titre if notion.theme and notion.theme.matiere else None,
            },
            'cours': cours_data,
            'synthese': synthese_data,
            'exercices': exercices_data,
            'demo_exercice_ids': demo_exercice_ids,
        })
