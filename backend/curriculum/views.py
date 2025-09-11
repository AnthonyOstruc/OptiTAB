"""
VUES HIÉRARCHIQUES PROFESSIONNELLES - Architecture REST cohérente
Structure: Pays → Niveau → Matière → Thème → Notion → Chapitre → Exercice
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from django.db import models
from django.core.cache import cache
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
import os
import base64
from io import BytesIO
import logging
from .models import Matiere, Theme, Notion, Chapitre, Exercice, MatiereContexte, ExerciceImage
from .serializers import (
    MatiereSerializer, ThemeSerializer, NotionSerializer, 
    ChapitreSerializer, ExerciceSerializer, MatiereContexteSerializer,
    ExerciceImageSerializer
)


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

        # Logs de debug (niveau debug seulement)
        logger.debug(
            "Filtrage themes/notions", 
            extra={
                'user': getattr(user, 'email', None),
                'user_pays': getattr(user_pays, 'id', None),
                'user_niveau': getattr(user_niveau, 'id', None),
                'matiere_id': matiere_id,
            }
        )

        # Clé de cache par utilisateur + contexte
        cache_key = f"themes_notions:{user.id}:{matiere_id or 'all'}:{getattr(user_pays, 'id', 'np')}:{getattr(user_niveau, 'id', 'nn')}"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        # Thèmes filtrés
        themes_qs = (
            Theme.objects.select_related('matiere', 'contexte', 'contexte__niveau', 'contexte__niveau__pays')
            .filter(est_actif=True)
        )
        if matiere_id:
            themes_qs = themes_qs.filter(matiere_id=matiere_id)
        if user_niveau:
            # Si l'utilisateur a un niveau spécifique, filtrer UNIQUEMENT par ce niveau
            themes_qs = themes_qs.filter(contexte__niveau=user_niveau).distinct()
        elif user_pays:
            # Si l'utilisateur n'a qu'un pays (sans niveau), filtrer par tous les niveaux de ce pays
            themes_qs = themes_qs.filter(contexte__niveau__pays=user_pays).distinct()
        else:
            # Aucun contexte défini -> aucun résultat
            themes_qs = themes_qs.none()

        # Annoter le nombre de notions actives
        themes_qs = themes_qs.annotate(
            notion_count=models.Count('notions', filter=models.Q(notions__est_actif=True), distinct=True)
        ).order_by('ordre', 'titre')

        # Notions pour ces thèmes (une seule requête)
        theme_ids = list(themes_qs.values_list('id', flat=True))
        notions_qs = (
            Notion.objects.select_related('theme', 'theme__matiere', 'theme__contexte', 'theme__contexte__niveau', 'theme__contexte__niveau__pays')
            .filter(est_actif=True, theme_id__in=theme_ids)
            .order_by('ordre', 'titre')
        )

        data = {
            'themes': ThemeSerializer(themes_qs.order_by('ordre', 'titre'), many=True).data,
            'notions': NotionSerializer(notions_qs, many=True).data,
        }

        # Cache 120s pour alléger la charge lors de navigations rapides
        cache.set(cache_key, data, timeout=120)
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

        if theme:
            queryset = queryset.filter(theme_id=theme)
        if matiere:
            queryset = queryset.filter(theme__matiere_id=matiere)
        # niveau param plus utilisé; filtrage par contexte se fait via Theme

        # Pour l'admin, ne pas filtrer par est_actif afin d'afficher toutes les notions
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated and (user.is_staff or user.is_superuser):
            return queryset.order_by('theme_id', 'ordre', 'titre')

        return queryset.filter(est_actif=True).order_by('ordre', 'titre')

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
    
    @action(detail=True, methods=['get'])
    def chapitres(self, request, pk=None):
        """GET /api/notions/{id}/chapitres/ - Récupère les chapitres d'une notion"""
        notion = self.get_object()
        chapitres = Chapitre.objects.filter(
            notion=notion,
            est_actif=True
        ).order_by('ordre', 'titre')
        
        serializer = ChapitreSerializer(chapitres, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='chapitres-avec-meta')
    def chapitres_avec_meta(self, request, pk=None):
        """GET /api/notions/{id}/chapitres-avec-meta/
        Retourne notion + chapitres dans une seule réponse. Cache 120s.
        """
        cache_key = f"chapitres_meta:{pk}"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        notion = self.get_object()
        chapitres = (
            Chapitre.objects.filter(notion=notion, est_actif=True)
            .order_by('ordre', 'titre')
        )
        data = {
            'notion': NotionSerializer(notion).data,
            'chapitres': ChapitreSerializer(chapitres, many=True).data,
        }
        cache.set(cache_key, data, timeout=120)
        return Response(data)


class ChapitreViewSet(viewsets.ModelViewSet):
    """ViewSet pour les chapitres avec actions hiérarchiques"""
    queryset = Chapitre.objects.all()
    serializer_class = ChapitreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée

    def get_queryset(self):
        queryset = super().get_queryset()
        notion = self.request.query_params.get('notion')
        
        if notion:
            queryset = queryset.filter(notion_id=notion)
            
        return queryset.filter(est_actif=True)
    
    @action(detail=True, methods=['get'])
    def exercices(self, request, pk=None):
        """GET /api/chapitres/{id}/exercices/ - Récupère les exercices d'un chapitre"""
        chapitre = self.get_object()
        exercices = Exercice.objects.filter(
            chapitre=chapitre,
            est_actif=True
        ).order_by('ordre', 'titre')
        
        serializer = ExerciceSerializer(exercices, many=True)
        return Response(serializer.data)


class ExerciceViewSet(viewsets.ModelViewSet):
    """ViewSet pour les exercices (ressource finale)"""
    queryset = Exercice.objects.all()
    serializer_class = ExerciceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée

    def get_queryset(self):
        queryset = super().get_queryset()
        chapitre = self.request.query_params.get('chapitre')
        
        if chapitre:
            queryset = queryset.filter(chapitre_id=chapitre)
            
        return queryset.filter(est_actif=True)

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        exercice_id = self.request.query_params.get('exercice')
        if exercice_id:
            queryset = queryset.filter(exercice_id=exercice_id)
        return queryset.order_by('position', 'id')