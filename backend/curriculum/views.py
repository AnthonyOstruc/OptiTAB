"""
VUES HIÉRARCHIQUES PROFESSIONNELLES - Architecture REST cohérente
Structure: Pays → Niveau → Matière → Thème → Notion → Chapitre → Exercice
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from django.db import models
from django.db import transaction
from django.core.cache import cache
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
import os
import base64
from io import BytesIO
import logging
from .models import Matiere, Theme, Notion, Exercice, MatiereContexte, ExerciceImage
from cours.models import Cours, CoursImage
from quiz.models import Quiz, QuizImage
from synthesis.models import SynthesisSheet
from .services import duplicate_theme_deep, duplicate_notion_deep
from .serializers import (
    MatiereSerializer, ThemeSerializer, NotionSerializer, 
    ExerciceSerializer, MatiereContexteSerializer,
    ExerciceImageSerializer
)

from subscriptions.permissions import HasActiveSubscriptionOrPass


logger = logging.getLogger(__name__)


class MatiereViewSet(viewsets.ModelViewSet):
    """ViewSet pour les matières"""
    queryset = Matiere.objects.filter(est_actif=True)
    serializer_class = MatiereSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        pays = self.request.query_params.get('pays')
        niveau = self.request.query_params.get('niveau')
        contexte = self.request.query_params.get('contexte')
        
        # Bypass filtering for admin users
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            if self.request.user.is_staff or self.request.user.is_superuser:
                # Admin users can see all matieres
                return queryset
        
        # Filtrage automatique par utilisateur connecté
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            # Matiere est désormais globale; le filtrage passe par MatiereContexte côté clients
            pass
        
        # Filtrage manuel par paramètres (pour admin ou override)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        # Accepter 'nom' comme alias de 'titre' côté admin/frontend
        mutable_data = request.data.copy()
        if 'nom' in mutable_data and 'titre' not in mutable_data:
            mutable_data['titre'] = mutable_data.pop('nom')
        request._full_data = mutable_data
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def admin_list(self, request):
        """Liste des matières pour l'interface d'administration"""
        # Pour l'admin, récupérer TOUTES les matières sans filtrage automatique
        matieres = Matiere.objects.filter(est_actif=True)
        
        admin_data = []
        for matiere in matieres:
            # Ajouter un aperçu des contextes liés pour faciliter l'admin frontend
            contextes = (
                matiere.contextes.select_related('niveau', 'niveau__pays')
                if hasattr(matiere, 'contextes') else []
            )
            admin_data.append({
                'id': matiere.id,
                'nom': matiere.titre,
                'description': matiere.description or '',
                'svg_icon': matiere.svg_icon or '',
                'ordre': matiere.ordre,
                'est_actif': matiere.est_actif,
                'show_on_home': getattr(matiere, 'show_on_home', True),
                'contextes': [
                    {
                        'id': c.id,
                        'niveau': {
                            'id': c.niveau.id,
                            'nom': c.niveau.nom,
                        },
                        'pays': {
                            'id': c.niveau.pays.id,
                            'nom': c.niveau.pays.nom,
                            'drapeau_emoji': getattr(c.niveau.pays, 'drapeau_emoji', '') or ''
                        }
                    } for c in contextes
                ]
            })
        
        return Response(admin_data)
    
    @action(detail=False, methods=['get'])
    def user_matieres(self, request):
        """Matières disponibles pour l'utilisateur connecté selon ses préférences pays/niveau"""
        if not request.user.is_authenticated:
            return Response({'error': 'Utilisateur non connecté'}, status=401)
        
        # Nouveau filtrage basé sur MatiereContexte
        user_pays = getattr(request.user, 'pays', None)
        user_niveau = getattr(request.user, 'niveau_pays', None)

        if not user_pays and not user_niveau:
            return Response({
                'user_pays': None,
                'user_niveau': None,
                'matieres_disponibles': [],
                'filtres_appliques': {
                    'pays': False,
                    'niveau': False
                },
                'message': "Veuillez configurer votre pays et niveau",
                'strict_fallback': False
            })

        contexte_qs = MatiereContexte.objects.filter(est_actif=True)
        if user_niveau:
            contexte_qs = contexte_qs.filter(niveau=user_niveau)
        elif user_pays:
            contexte_qs = contexte_qs.filter(niveau__pays=user_pays)

        matiere_ids = contexte_qs.values_list('matiere_id', flat=True).distinct()
        matieres = Matiere.objects.filter(id__in=matiere_ids, est_actif=True).order_by('ordre', 'titre')
        
        user_data = {
            'user_pays': {
                'id': user_pays.id,
                'nom': user_pays.nom,
                'drapeau_emoji': user_pays.drapeau_emoji
            } if user_pays else None,
            'user_niveau': {
                'id': user_niveau.id,
                'nom': user_niveau.nom,
                'pays': {
                    'id': user_niveau.pays.id,
                    'nom': user_niveau.pays.nom,
                    'drapeau_emoji': user_niveau.pays.drapeau_emoji
                }
            } if user_niveau else None,
            'matieres_disponibles': [],
            'filtres_appliques': {
                'pays': bool(user_pays),
                'niveau': bool(user_niveau)
            },
            'message': 'Matières filtrées via vos préférences (contexte matière+niveau)',
            'strict_fallback': False
        }
        
        for matiere in matieres:
            user_data['matieres_disponibles'].append({
                'id': matiere.id,
                'nom': matiere.titre,
                'description': matiere.description or '',
                'svg_icon': matiere.svg_icon or '',
                'ordre': matiere.ordre,
                'couleur': matiere.couleur
            })
        
        return Response(user_data)
    
    @action(detail=False, methods=['get'])
    def matieres_filtrees(self, request):
        """Matières filtrées selon les paramètres de requête (pays et niveau)"""
        pays_id = request.query_params.get('pays')
        niveau_id = request.query_params.get('niveau')
        
        queryset = super().get_queryset()
        
        # Appliquer les filtres si fournis
        if pays_id and niveau_id:
            # FILTRAGE STRICT : Matières qui correspondent AU PAYS ET AU NIVEAU
            queryset = queryset.filter(
                Q(pays=pays_id) & Q(niveaux=niveau_id)
            ).distinct()
        elif pays_id:
            queryset = queryset.filter(
                Q(pays=pays_id) | Q(niveaux__pays=pays_id)
            ).distinct()
        elif niveau_id:
            queryset = queryset.filter(niveaux=niveau_id)
        
        # Préparer les données de réponse
        matieres_data = []
        for matiere in queryset.prefetch_related('pays', 'niveaux', 'niveaux__pays'):
            pays_matiere = [{'id': p.id, 'nom': p.nom, 'drapeau_emoji': p.drapeau_emoji} for p in matiere.pays.all()]
            niveaux_matiere = [{'id': n.id, 'nom': n.nom, 'pays': {'id': n.pays.id, 'nom': n.pays.nom, 'drapeau_emoji': n.pays.drapeau_emoji}} for n in matiere.niveaux.all()]
            
            matieres_data.append({
                'id': matiere.id,
                'nom': matiere.titre,
                'description': matiere.description or '',
                'svg_icon': matiere.svg_icon or '',
                'ordre': matiere.ordre,
                'couleur': matiere.couleur,
                'pays_associes': pays_matiere,
                'niveaux_associes': niveaux_matiere,
                'pays_count': matiere.pays_count,
                'niveaux_count': matiere.niveaux_count
            })
        
        response_data = {
            'matieres': matieres_data,
            'filtres_appliques': {
                'pays_id': pays_id,
                'niveau_id': niveau_id
            },
            'total': len(matieres_data)
        }
        
        return Response(response_data)
    


class MatiereContexteViewSet(viewsets.ModelViewSet):
    """CRUD pour les contextes Matière+Niveau

    Permet de créer Mathématiques (France, 5ème) et de rattacher tout le contenu dessous.
    """
    queryset = (
        MatiereContexte.objects.select_related('matiere', 'niveau', 'niveau__pays')
        .filter(est_actif=True)
        .order_by('matiere__ordre', 'niveau__pays__nom', 'niveau__ordre')
    )
    serializer_class = MatiereContexteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        matiere = self.request.query_params.get('matiere')
        pays = self.request.query_params.get('pays')
        niveau = self.request.query_params.get('niveau')
        if matiere:
            qs = qs.filter(matiere_id=matiere)
        if niveau:
            qs = qs.filter(niveau_id=niveau)
        if pays:
            qs = qs.filter(niveau__pays_id=pays)
        return qs

    @action(detail=False, methods=['get'], url_path='pour-utilisateur')
    def pour_utilisateur(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return Response({'detail': 'Authentification requise'}, status=status.HTTP_401_UNAUTHORIZED)
        user_pays = getattr(user, 'pays', None)
        user_niveau = getattr(user, 'niveau_pays', None)
        qs = MatiereContexte.objects.select_related('matiere', 'niveau', 'niveau__pays').filter(est_actif=True)
        if user_niveau:
            qs = qs.filter(niveau=user_niveau)
        elif user_pays:
            qs = qs.filter(niveau__pays=user_pays)
        else:
            qs = qs.none()
        serializer = MatiereContexteSerializer(qs, many=True)
        return Response(serializer.data)


class ThemeViewSet(viewsets.ModelViewSet):
    """ViewSet pour les thèmes avec actions hiérarchiques"""
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related('matiere', 'contexte', 'contexte__niveau', 'contexte__niveau__pays')
        )
        matiere = self.request.query_params.get('matiere')
        pays = self.request.query_params.get('pays')
        niveau = self.request.query_params.get('niveau')
        contexte = self.request.query_params.get('contexte')

        if matiere:
            queryset = queryset.filter(matiere_id=matiere)
        if contexte:
            queryset = queryset.filter(contexte_id=contexte)
        if niveau:
            queryset = queryset.filter(contexte__niveau_id=niveau)
        if pays:
            queryset = queryset.filter(contexte__niveau__pays_id=pays)

        queryset = queryset.filter(est_actif=True).annotate(
            notion_count=models.Count('notions', filter=models.Q(notions__est_actif=True), distinct=True)
        )
        return queryset.order_by('ordre', 'titre')
    
    @action(detail=False, methods=['get'], url_path='pour-utilisateur')
    def pour_utilisateur(self, request):
        """GET /api/themes/pour-utilisateur/ - Thèmes filtrés par pays/niveau de l'utilisateur
        Optionnellement, filtrer par matière via ?matiere=<id>
        """
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentification requise'}, status=status.HTTP_401_UNAUTHORIZED)

        user_pays = getattr(request.user, 'pays', None)
        user_niveau = getattr(request.user, 'niveau_pays', None)

        queryset = (
            Theme.objects.select_related('matiere', 'contexte', 'contexte__niveau', 'contexte__niveau__pays')
            .filter(est_actif=True)
        )

        # Filtre optionnel par matière
        matiere_id = request.query_params.get('matiere')
        if matiere_id:
            queryset = queryset.filter(matiere_id=matiere_id)

        # Appliquer les filtres via le contexte (niveau → pays)
        if user_niveau:
            queryset = queryset.filter(
                models.Q(contexte__niveau=user_niveau) | models.Q(contexte__niveau__pays=user_pays)
            ).distinct()
        elif user_pays:
            queryset = queryset.filter(contexte__niveau__pays=user_pays).distinct()
        else:
            queryset = queryset.none()

        # Annoter le nombre de notions pour chaque thème
        queryset = queryset.annotate(
            notion_count=models.Count('notions', filter=models.Q(notions__est_actif=True), distinct=True)
        ).order_by('ordre', 'titre')
        serializer = ThemeSerializer(queryset.order_by('ordre', 'titre'), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """POST /api/themes/{id}/duplicate/
        Duplique un thème et tout son contenu imbriqué (notions, chapitres, cours, quiz,
        exercices, fiches de synthèse et images) vers un nouveau contexte.

        Body JSON:
          - contexte (int, requis): ID du `MatiereContexte` cible
          - titre|nom (str, optionnel): nouveau titre du thème (sinon suffixe "(Copie)")
        """
        # Récupérer l'original sans filtrage
        try:
            original = Theme.objects.select_related('matiere', 'contexte').get(pk=pk)
        except Theme.DoesNotExist:
            return Response({'detail': 'Thème introuvable'}, status=status.HTTP_404_NOT_FOUND)

        target_contexte_id = request.data.get('contexte')
        new_title = (request.data.get('titre') or request.data.get('nom') or '').strip()

        if not target_contexte_id:
            return Response({'detail': "Le champ 'contexte' est requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_contexte = MatiereContexte.objects.get(pk=target_contexte_id)
        except MatiereContexte.DoesNotExist:
            return Response({'detail': 'Contexte cible introuvable'}, status=status.HTTP_404_NOT_FOUND)

        # Générer un titre unique dans le contexte cible
        base_title = new_title or (original.titre or 'Thème')

        def generate_unique_title(base: str) -> str:
            candidate = base
            index = 1
            while Theme.objects.filter(contexte=target_contexte, titre=candidate).exists():
                suffix = '' if index == 1 else f' {index}'
                candidate = f"{base} (Copie{suffix})"
                index += 1
            return candidate

        unique_title = generate_unique_title(base_title)

        # Dupliquer via le service centralisé
        new_theme = duplicate_theme_deep(original, target_contexte, unique_title)

        serializer = ThemeSerializer(new_theme)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='notions-pour-utilisateur')
    def notions_pour_utilisateur(self, request):
        """GET /api/themes/notions-pour-utilisateur/
        Retourne en une seule réponse les thèmes et les notions accessibles
        à l'utilisateur courant, optionnellement filtrés par matière via ?matiere=<id>.

        Optimisé avec select_related/prefetch et un cache court (120s) par utilisateur/contexte.
        """
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return Response({'detail': 'Authentification requise'}, status=status.HTTP_401_UNAUTHORIZED)

        user_pays = getattr(user, 'pays', None)
        user_niveau = getattr(user, 'niveau_pays', None)
        matiere_id = request.query_params.get('matiere')

        # Clé de cache par utilisateur + contexte
        cache_key = f"themes_notions:{user.id}:{matiere_id or 'all'}:{getattr(user_pays, 'id', 'np')}:{getattr(user_niveau, 'id', 'nn')}"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        # Construire le queryset de base pour les notions (filtré par pays/niveau)
        notions_base_qs = Notion.objects.filter(est_actif=True)
        
        # Appliquer les filtres contexte sur les notions directement
        if user_niveau:
            notions_base_qs = notions_base_qs.filter(theme__contexte__niveau=user_niveau)
        elif user_pays:
            notions_base_qs = notions_base_qs.filter(theme__contexte__niveau__pays=user_pays)
        else:
            notions_base_qs = notions_base_qs.none()

        if matiere_id:
            notions_base_qs = notions_base_qs.filter(theme__matiere_id=matiere_id)

        # Récupérer les IDs des thèmes qui ont des notions actives (une seule requête)
        theme_ids_with_notions = list(notions_base_qs.values_list('theme_id', flat=True).distinct())

        # Thèmes filtrés (seulement ceux qui ont des notions)
        themes_qs = (
            Theme.objects
            .select_related('matiere', 'contexte')
            .filter(id__in=theme_ids_with_notions, est_actif=True)
            .annotate(
                notion_count=models.Count('notions', filter=models.Q(notions__est_actif=True), distinct=True)
            )
            .order_by('ordre', 'titre')
        )

        # Notions avec sélection minimale des relations
        notions_qs = notions_base_qs.select_related('theme').order_by('theme_id', 'ordre', 'titre')

        # Sérialiser en une seule fois (plus rapide)
        themes_data = ThemeSerializer(themes_qs, many=True).data
        notions_data = NotionSerializer(notions_qs, many=True).data

        data = {
            'themes': themes_data,
            'notions': notions_data,
        }

        # Cache 300s (5 minutes) pour alléger la charge lors de navigations rapides
        cache.set(cache_key, data, timeout=300)
        return Response(data)

    @action(detail=True, methods=['get'])
    def notions(self, request, pk=None):
        """GET /api/themes/{id}/notions/ - Récupère les notions d'un thème"""
        theme = self.get_object()
        notions = Notion.objects.filter(
            theme=theme,
            est_actif=True
        ).order_by('ordre', 'titre')
        
        serializer = NotionSerializer(notions, many=True)
        return Response(serializer.data)


class NotionViewSet(viewsets.ModelViewSet):
    """ViewSet pour les notions avec actions hiérarchiques"""
    queryset = Notion.objects.all()
    serializer_class = NotionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related('theme', 'theme__matiere')
        )
        theme = self.request.query_params.get('theme')
        matiere = self.request.query_params.get('matiere')
        niveau = self.request.query_params.get('niveau')
        contexte = self.request.query_params.get('contexte')
        search = self.request.query_params.get('search') or self.request.query_params.get('q')

        if theme:
            queryset = queryset.filter(theme_id=theme)
        if matiere:
            queryset = queryset.filter(theme__matiere_id=matiere)
        if contexte:
            queryset = queryset.filter(theme__contexte_id=contexte)
        if search:
            queryset = queryset.filter(titre__icontains=search)
        # niveau param plus utilisé; filtrage par contexte se fait via Theme

        # Pour l'admin, ne pas filtrer par est_actif afin d'afficher toutes les notions
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and (user.is_staff or user.is_superuser):
            return queryset.order_by('theme_id', 'ordre', 'titre')

        return queryset.filter(est_actif=True).order_by('ordre', 'titre')

    def list(self, request, *args, **kwargs):
        """Supporte une pagination simple via ?limit=5&offset=0 pour l'admin."""
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

    def partial_update(self, request, *args, **kwargs):
        # Accepter 'nom' comme alias de 'titre' côté admin/frontend
        mutable_data = request.data.copy()
        if 'nom' in mutable_data and 'titre' not in mutable_data:
            mutable_data['titre'] = mutable_data.pop('nom')
        request._full_data = mutable_data
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Alias 'nom' → 'titre'
        mutable_data = request.data.copy()
        if 'nom' in mutable_data and 'titre' not in mutable_data:
            mutable_data['titre'] = mutable_data.pop('nom')
        request._full_data = mutable_data
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='pour-utilisateur')
    def pour_utilisateur(self, request):
        """GET /api/notions/pour-utilisateur/ - Notions filtrées par pays/niveau de l'utilisateur
        Paramètres optionnels:
          - matiere: limiter aux notions dont le thème appartient à cette matière
          - theme: limiter aux notions de ce thème
        """
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentification requise'}, status=status.HTTP_401_UNAUTHORIZED)

        user_pays = getattr(request.user, 'pays', None)
        user_niveau = getattr(request.user, 'niveau_pays', None)

        queryset = (
            Notion.objects.select_related('theme', 'theme__matiere')
            .filter(est_actif=True)
        )

        # Filtres optionnels de périmètre
        theme_id = request.query_params.get('theme')
        matiere_id = request.query_params.get('matiere')
        if theme_id:
            queryset = queryset.filter(theme_id=theme_id)
        if matiere_id:
            queryset = queryset.filter(theme__matiere_id=matiere_id)

        # Appliquer les filtres pays/niveau de l'utilisateur
        if user_niveau:
            queryset = queryset.filter(
                models.Q(theme__contexte__niveau=user_niveau)
                | models.Q(theme__contexte__niveau__pays=user_pays)
            ).distinct()
        elif user_pays:
            queryset = queryset.filter(
                models.Q(theme__contexte__niveau__pays=user_pays)
            ).distinct()
        else:
            queryset = queryset.none()

        serializer = NotionSerializer(queryset.order_by('ordre', 'titre'), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """POST /api/notions/{id}/duplicate/
        Duplique une notion et tout son contenu (synthèse, chapitres, cours, quiz, exercices et images)
        dans un thème cible.

        Body JSON:
          - theme (int, requis): ID du `Theme` cible
          - titre|nom (str, optionnel): nouveau titre de la notion (suffixe "(Copie)" si nécessaire)
        """
        try:
            original = Notion.objects.select_related('theme', 'theme__matiere').get(pk=pk)
        except Notion.DoesNotExist:
            return Response({'detail': 'Notion introuvable'}, status=status.HTTP_404_NOT_FOUND)

        target_theme_id = request.data.get('theme')
        new_title = (request.data.get('titre') or request.data.get('nom') or '').strip()

        if not target_theme_id:
            return Response({'detail': "Le champ 'theme' est requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_theme = Theme.objects.get(pk=target_theme_id)
        except Theme.DoesNotExist:
            return Response({'detail': 'Thème cible introuvable'}, status=status.HTTP_404_NOT_FOUND)

        # Dupliquer via le service
        new_notion = duplicate_notion_deep(original, target_theme, new_title or None)

        serializer = NotionSerializer(new_notion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ExerciceViewSet(viewsets.ModelViewSet):
    """ViewSet pour les exercices (ressource finale)"""
    queryset = Exercice.objects.all()
    serializer_class = ExerciceSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasActiveSubscriptionOrPass()]

    def get_queryset(self):
        queryset = super().get_queryset()
        notion = self.request.query_params.get('notion')
        matiere = self.request.query_params.get('matiere')
        search = self.request.query_params.get('search') or self.request.query_params.get('q')
        
        if notion:
            queryset = queryset.filter(notion_id=notion)
        if matiere:
            queryset = queryset.filter(notion__theme__matiere_id=matiere)
        if search:
            queryset = queryset.filter(models.Q(titre__icontains=search) | models.Q(question__icontains=search))
            
        # L'exercice n'a pas de champ "ordre"; on garde un tri stable par notion puis titre/id.
        return (
            queryset
            .select_related('notion', 'notion__theme', 'notion__theme__matiere')
            .filter(est_actif=True)
            .order_by('notion_id', 'titre', 'id')
        )

    def list(self, request, *args, **kwargs):
        """Supporte une pagination simple via ?limit=5&offset=0 pour l'admin."""
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

    @action(detail=True, methods=['get'], url_path='pdf')
    def pdf_single(self, request, pk=None):
        """Génère un PDF propre (énoncé seul ou corrigé) côté backend via Playwright + MathJax.

        Paramètres:
          - include_solution: '1' ou '0' (par défaut: 0)
        """
        include_solution = request.query_params.get('include_solution', '0') == '1'
        exercice = self.get_object()

        # Construire HTML minimal avec MathJax et style propre
        html = render_to_string('curriculum/exercice_pdf.html', {
            'exercice': exercice,
            'include_solution': include_solution,
        })

        # Rendu PDF via Playwright (Chromium headless)
        try:
            from playwright.sync_api import sync_playwright
        except Exception as e:
            return Response({'detail': 'Playwright non installé côté serveur'}, status=500)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html, wait_until='load')
            # Attendre que MathJax finisse
            page.wait_for_function("() => window.MathJax && MathJax.startup && MathJax.startup.promise")
            page.evaluate("() => MathJax.startup.promise")
            # Laisser un léger délai pour stabiliser
            page.wait_for_timeout(500)
            pdf_bytes = page.pdf(format='A4', margin={'top': '12mm', 'right': '12mm', 'bottom': '12mm', 'left': '12mm'}, print_background=True)
            browser.close()

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        title = f"Exercice_{exercice.id}{'_corrige' if include_solution else ''}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{title}"'
        return response


class ExerciceImageViewSet(viewsets.ModelViewSet):
    """CRUD pour les images d'exercice

    Frontend attends /api/exercice-images/ avec filtre ?exercice=<id>
    """
    queryset = ExerciceImage.objects.all()
    serializer_class = ExerciceImageSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_permissions(self):
        """Lecture protégée par abonnement, modifications réservées aux utilisateurs authentifiés (admin)."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasActiveSubscriptionOrPass()]

    def get_queryset(self):
        queryset = super().get_queryset()
        exercice_id = self.request.query_params.get('exercice')
        if exercice_id:
            queryset = queryset.filter(exercice_id=exercice_id)
        return queryset.order_by('position', 'id')

    def create(self, request, *args, **kwargs):
        """Créer une image d'exercice avec upload de fichier"""
        # Vérifier que l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentification requise pour uploader des images'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Créer l'instance via le serializer avec les données de la requête
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
