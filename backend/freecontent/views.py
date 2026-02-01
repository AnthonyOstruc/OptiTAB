import re
from django.db.models import Q, Count, Case, When, Value, BooleanField, F
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from cours.models import Cours
from curriculum.models import Exercice
from synthesis.models import SynthesisSheet
from .models import FreeLearningResource
from .serializers import (
    FreeLearningResourceSerializer,
    CourseFreePreviewSerializer,
    ExerciceFreePreviewSerializer,
    SynthesisFreePreviewSerializer,
    ExerciseNotionSummarySerializer
)

SEARCH_STOPWORDS = {
    'a',
    'au',
    'aux',
    'avec',
    'chez',
    'dans',
    'de',
    'des',
    'du',
    'en',
    'et',
    'l',
    'la',
    'le',
    'les',
    'd',
    'cours',
    'exercice',
    'exercices',
    'fiche',
    'fiches',
    'resume',
    'résumé',
    'synthese',
    'synthèse',
    'enligne',
    'ligne',
    'online',
    'gratuit',
    'gratuits',
    'gratuite',
    'gratuites',
    'gratuitement',
    'corrige',
    'corriges',
    'corrigee',
    'corrigees',
    'corrigé',
    'corrigés',
    'corrigée',
    'corrigées',
    'programme',
}

SEARCH_SYNONYMS = {
    'maths': ['maths', 'math', 'mathematique', 'mathematiques', 'mathématique', 'mathématiques'],
    'math': ['math', 'maths', 'mathematique', 'mathematiques', 'mathématique', 'mathématiques'],
    'mathematique': ['mathematique', 'mathematiques', 'mathématique', 'mathématiques', 'maths', 'math'],
    'mathematiques': ['mathematiques', 'mathematique', 'mathématiques', 'mathématique', 'maths', 'math'],
    'terminal': ['terminal', 'terminale', 'tle'],
    'terminale': ['terminale', 'terminal', 'tle'],
    'premiere': ['premiere', 'première', '1ere', '1ère', '1re'],
    'première': ['première', 'premiere', '1ere', '1ère', '1re'],
    'seconde': ['seconde', '2nde', '2de'],
    '2nde': ['2nde', '2de', 'seconde'],
    '2de': ['2de', '2nde', 'seconde'],
    'physique': ['physique'],
    'chimie': ['chimie'],
    'informatique': ['informatique'],
}


def _tokenize_search(value):
    text = str(value or '').strip().lower()
    if not text:
        return []
    # Supporte accents + chiffres (1ere, 2nde...)
    tokens = re.findall(r"[0-9a-zà-ÿ]+", text)
    cleaned = []
    for token in tokens:
        if len(token) < 2:
            continue
        if token in SEARCH_STOPWORDS:
            continue
        cleaned.append(token)

    # Dédupliquer en conservant l'ordre pour éviter des Q() énormes
    seen = set()
    unique = []
    for token in cleaned:
        if token in seen:
            continue
        seen.add(token)
        unique.append(token)
    return unique[:8]


def _expand_search_token(token):
    if not token:
        return []
    if token in SEARCH_SYNONYMS:
        return SEARCH_SYNONYMS[token]
    # Tolérance simple pour les petites erreurs ("emaths" -> "maths")
    if token.startswith('e') and len(token) > 3:
        maybe = token[1:]
        if maybe in SEARCH_SYNONYMS:
            return SEARCH_SYNONYMS[maybe]
        return [token, maybe]
    return [token]


def build_search_q(value, fields):
    tokens = _tokenize_search(value)
    if not tokens or not fields:
        return None
    query = Q()
    for token in tokens:
        variants = _expand_search_token(token)
        token_q = Q()
        for variant in variants:
            for field in fields:
                token_q |= Q(**{f'{field}__icontains': variant})
        query &= token_q
    return query


class FreeLearningResourcePagination(PageNumberPagination):
    """Pagination simple pour limiter la payload des ressources gratuites."""

    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 500


class FreeLearningResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API publique pour lister les ressources gratuites (cours, resumes, exercices).

    Aucun jeton requis : ces ressources servent a rassurer avant abonnement.
    """

    serializer_class = FreeLearningResourceSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    pagination_class = FreeLearningResourcePagination
    queryset = (
        FreeLearningResource.objects
        .filter(est_actif=True, est_publie=True)
        .select_related(
            'matiere',
            'niveau',
            'niveau__pays',
            'notion',
            'notion__theme',
            'notion__theme__matiere',
            'notion__theme__contexte',
            'notion__theme__contexte__niveau',
            'notion__theme__contexte__niveau__pays',
        )
        .order_by('resource_type', 'ordre', '-date_modification')
    )

    def get_queryset(self):
        qs = self.queryset
        params = self.request.query_params

        resource_type = params.get('type') or params.get('resource_type')
        matiere_id = params.get('matiere')
        niveau_id = params.get('niveau')
        notion_id = params.get('notion')
        pays_id = params.get('pays')
        search = params.get('q')

        if resource_type:
            qs = qs.filter(resource_type=resource_type)
        if matiere_id:
            qs = qs.filter(matiere_id=matiere_id)
        if niveau_id:
            qs = qs.filter(niveau_id=niveau_id)
        if notion_id:
            qs = qs.filter(notion_id=notion_id)
        if pays_id:
            qs = qs.filter(niveau__pays_id=pays_id)
        if search:
            search_q = build_search_q(search, [
                'titre',
                'excerpt',
                'accroche',
                'contenu_html',
                'matiere__titre',
                'niveau__nom',
                'niveau__pays__nom',
                'notion__titre',
            ])
            if search_q:
                qs = qs.filter(search_q)

        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def list(self, request, *args, **kwargs):
        resource_type = request.query_params.get('type') or request.query_params.get('resource_type')

        if resource_type == FreeLearningResource.TYPE_COURSE:
            queryset = self._apply_limit(self._get_free_courses_queryset(request), request)
            return self._paginate_and_serialize(queryset, CourseFreePreviewSerializer)
        if resource_type == FreeLearningResource.TYPE_EXERCISE:
            group_param = request.query_params.get('group_by') or request.query_params.get('group') or ''
            group_by_notion = str(group_param).lower() == 'notion'
            group_flag = str(request.query_params.get('group_by_notion', '')).lower() in ('1', 'true', 'yes')
            if group_by_notion or group_flag:
                return self._list_free_exercises_grouped(request)
            queryset = self._apply_limit(self._get_free_exercises_queryset(request), request)
            return self._paginate_and_serialize(queryset, ExerciceFreePreviewSerializer)
        if resource_type == FreeLearningResource.TYPE_SUMMARY:
            queryset = self._apply_limit(self._get_free_summaries_queryset(request), request)
            return self._paginate_and_serialize(queryset, SynthesisFreePreviewSerializer)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = self._apply_limit(queryset, request)

        serializer_class = self.get_serializer_class()
        return self._paginate_and_serialize(queryset, serializer_class)

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get(self.lookup_field)

        def parse_prefixed_id(value, prefix):
            if not value:
                return None
            match = re.match(rf'^{re.escape(prefix)}-(\d+)', str(value))
            if not match:
                return None
            try:
                return int(match.group(1))
            except (TypeError, ValueError):
                return None

        if slug and slug.startswith('cours-gratuit-'):
            try:
                course_id = parse_prefixed_id(slug, 'cours-gratuit')
                if course_id is None:
                    raise ValueError()
            except ValueError:
                raise NotFound("Cours gratuit introuvable.")
            cours = Cours.objects.filter(
                pk=course_id,
                est_actif=True,
                access_scope__in=[Cours.ACCESS_SCOPE_FREE, Cours.ACCESS_SCOPE_BOTH]
            ).select_related(
                'notion',
                'notion__theme',
                'notion__theme__matiere',
                'notion__theme__contexte',
                'notion__theme__contexte__niveau',
                'notion__theme__contexte__niveau__pays',
            ).first()
            if not cours:
                raise NotFound("Cours gratuit introuvable.")
            data = CourseFreePreviewSerializer().to_representation(cours)
            return Response(data)
        if slug and slug.startswith('exercice-gratuit-'):
            try:
                exercice_id = parse_prefixed_id(slug, 'exercice-gratuit')
                if exercice_id is None:
                    raise ValueError()
            except ValueError:
                raise NotFound("Exercice gratuit introuvable.")
            exercice = Exercice.objects.filter(
                pk=exercice_id,
                est_actif=True,
                access_scope__in=[Exercice.ACCESS_SCOPE_FREE, Exercice.ACCESS_SCOPE_BOTH]
            ).select_related(
                'notion',
                'notion__theme',
                'notion__theme__matiere',
                'notion__theme__contexte',
                'notion__theme__contexte__niveau',
                'notion__theme__contexte__niveau__pays',
            ).prefetch_related('images').first()
            if not exercice:
                raise NotFound("Exercice gratuit introuvable.")
            serializer = ExerciceFreePreviewSerializer(exercice, context=self.get_serializer_context())
            return Response(serializer.data)
        if slug and slug.startswith('synthese-gratuite-'):
            try:
                sheet_id = parse_prefixed_id(slug, 'synthese-gratuite')
                if sheet_id is None:
                    raise ValueError()
            except ValueError:
                raise NotFound("Résumé gratuit introuvable.")
            sheet = (
                SynthesisSheet.objects.filter(
                    pk=sheet_id,
                    est_actif=True,
                    access_scope__in=[SynthesisSheet.ACCESS_SCOPE_FREE, SynthesisSheet.ACCESS_SCOPE_BOTH]
                )
                .select_related(
                    'notion',
                    'notion__theme',
                    'notion__theme__matiere',
                    'notion__theme__contexte',
                    'notion__theme__contexte__niveau',
                    'notion__theme__contexte__niveau__pays'
                )
                .prefetch_related('images')
                .first()
            )
            if not sheet:
                raise NotFound("Résumé gratuit introuvable.")
            serializer = SynthesisFreePreviewSerializer(sheet, context=self.get_serializer_context())
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)

    def _get_free_courses_queryset(self, request):
        qs = (
            Cours.objects.filter(est_actif=True)
            .select_related(
                'notion',
                'notion__theme',
                'notion__theme__matiere',
                'notion__theme__contexte',
                'notion__theme__contexte__niveau',
                'notion__theme__contexte__niveau__pays',
            )
            .prefetch_related('images')
            .annotate(
                is_locked=Case(
                    When(access_scope=Cours.ACCESS_SCOPE_PAID, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
            .order_by('is_locked', 'ordre', 'notion__titre')
        )

        params = request.query_params
        matiere_id = params.get('matiere')
        niveau_id = params.get('niveau')
        niveau_names = (
            params.getlist('niveau_nom')
            or params.getlist('niveau_nom[]')
            or []
        )
        if len(niveau_names) == 1 and ',' in niveau_names[0]:
            # Support ?niveau_nom=a,b,c
            niveau_names = [v.strip() for v in niveau_names[0].split(',') if v.strip()]
        elif not niveau_names and params.get('niveau_nom'):
            # Fallback simple
            niveau_names = [v.strip() for v in params.get('niveau_nom', '').split(',') if v.strip()]
        notion_id = params.get('notion')
        pays_id = params.get('pays')
        search = params.get('q')

        if matiere_id:
            qs = qs.filter(notion__theme__matiere_id=matiere_id)
        if niveau_id:
            qs = qs.filter(notion__theme__contexte__niveau_id=niveau_id)
        if niveau_names:
            qs = qs.filter(notion__theme__contexte__niveau__nom__in=niveau_names)
        if notion_id:
            qs = qs.filter(notion_id=notion_id)
        if pays_id:
            qs = qs.filter(notion__theme__contexte__niveau__pays_id=pays_id)
        if search:
            search_q = build_search_q(search, [
                'titre',
                'contenu',
                'notion__titre',
                'notion__theme__matiere__titre',
                'notion__theme__contexte__niveau__nom',
                'notion__theme__contexte__niveau__pays__nom',
            ])
            if search_q:
                qs = qs.filter(search_q)

        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def _list_free_exercises_grouped(self, request):
        """
        Retourne une pagination par notion (chapitre) avec le nombre d'exercices et le statut de verrou.
        """
        base_queryset = self._get_free_exercises_queryset(request)
        total_exercises = base_queryset.count()

        grouped_qs = (
            base_queryset
            .values(
                'notion',
                'notion__titre',
                'notion__theme__matiere__titre',
                'notion__theme__contexte__niveau__nom',
                'notion__theme__contexte__niveau__pays__nom',
            )
            .annotate(
                count=Count('id'),
                free_count=Count('id', filter=Q(access_scope__in=[Exercice.ACCESS_SCOPE_FREE, Exercice.ACCESS_SCOPE_BOTH])),
                notion_nom=F('notion__titre'),
                matiere_nom=F('notion__theme__matiere__titre'),
                niveau_nom=F('notion__theme__contexte__niveau__nom'),
                pays_nom=F('notion__theme__contexte__niveau__pays__nom'),
                tag_secondaire=F('notion__theme__contexte__niveau__nom'),
            )
            .annotate(
                is_locked=Case(
                    When(free_count__gt=0, then=Value(False)),
                    default=Value(True),
                    output_field=BooleanField()
                )
            )
            .order_by('is_locked', 'notion__titre', 'notion')
        )

        grouped_qs = self._apply_limit(grouped_qs, request)

        page = self.paginate_queryset(grouped_qs)
        serializer = ExerciseNotionSummarySerializer(page or grouped_qs, many=True, context=self.get_serializer_context())

        if page is not None:
            response = self.get_paginated_response(serializer.data)
            response.data['total_exercises'] = total_exercises
            return response

        return Response(serializer.data)

    def _paginate_and_serialize(self, queryset, serializer_class):
        """Applique la pagination standard et serialise le resultat."""
        page = self.paginate_queryset(queryset)
        context = self.get_serializer_context()
        if page is not None:
            serializer = serializer_class(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        serializer = serializer_class(queryset, many=True, context=context)
        return Response(serializer.data)

    def _get_free_exercises_queryset(self, request):
        qs = (
            Exercice.objects.filter(est_actif=True)
            .select_related(
                'notion',
                'notion__theme',
                'notion__theme__matiere',
                'notion__theme__contexte',
                'notion__theme__contexte__niveau',
                'notion__theme__contexte__niveau__pays',
            )
            .prefetch_related('images')
            .annotate(
                is_locked=Case(
                    When(access_scope=Exercice.ACCESS_SCOPE_PAID, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
            .order_by('is_locked', 'notion__titre', 'id')
        )

        params = request.query_params
        matiere_id = params.get('matiere')
        niveau_id = params.get('niveau')
        niveau_names = (
            params.getlist('niveau_nom')
            or params.getlist('niveau_nom[]')
            or []
        )
        if len(niveau_names) == 1 and ',' in niveau_names[0]:
            niveau_names = [v.strip() for v in niveau_names[0].split(',') if v.strip()]
        elif not niveau_names and params.get('niveau_nom'):
            niveau_names = [v.strip() for v in params.get('niveau_nom', '').split(',') if v.strip()]
        notion_id = params.get('notion')
        pays_id = params.get('pays')
        search = params.get('q')

        if matiere_id:
            qs = qs.filter(notion__theme__matiere_id=matiere_id)
        if niveau_id:
            qs = qs.filter(notion__theme__contexte__niveau_id=niveau_id)
        if niveau_names:
            qs = qs.filter(notion__theme__contexte__niveau__nom__in=niveau_names)
        if notion_id:
            qs = qs.filter(notion_id=notion_id)
        if pays_id:
            qs = qs.filter(notion__theme__contexte__niveau__pays_id=pays_id)
        if search:
            search_q = build_search_q(search, [
                'titre',
                'contenu',
                'question',
                'notion__titre',
                'notion__theme__matiere__titre',
                'notion__theme__contexte__niveau__nom',
                'notion__theme__contexte__niveau__pays__nom',
            ])
            if search_q:
                qs = qs.filter(search_q)

        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def _get_free_summaries_queryset(self, request):
        qs = (
            SynthesisSheet.objects.filter(est_actif=True)
            .select_related(
                'notion',
                'notion__theme',
                'notion__theme__matiere',
                'notion__theme__contexte',
                'notion__theme__contexte__niveau',
                'notion__theme__contexte__niveau__pays',
            )
            .prefetch_related('images')
            .annotate(
                is_locked=Case(
                    When(access_scope=SynthesisSheet.ACCESS_SCOPE_PAID, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
            .order_by('is_locked', 'ordre', 'notion__titre')
        )

        params = request.query_params
        matiere_id = params.get('matiere')
        niveau_id = params.get('niveau')
        niveau_names = (
            params.getlist('niveau_nom')
            or params.getlist('niveau_nom[]')
            or []
        )
        if len(niveau_names) == 1 and ',' in niveau_names[0]:
            niveau_names = [v.strip() for v in niveau_names[0].split(',') if v.strip()]
        elif not niveau_names and params.get('niveau_nom'):
            niveau_names = [v.strip() for v in params.get('niveau_nom', '').split(',') if v.strip()]
        notion_id = params.get('notion')
        pays_id = params.get('pays')
        search = params.get('q')

        if matiere_id:
            qs = qs.filter(notion__theme__matiere_id=matiere_id)
        if niveau_id:
            qs = qs.filter(notion__theme__contexte__niveau_id=niveau_id)
        if niveau_names:
            qs = qs.filter(notion__theme__contexte__niveau__nom__in=niveau_names)
        if notion_id:
            qs = qs.filter(notion_id=notion_id)
        if pays_id:
            qs = qs.filter(notion__theme__contexte__niveau__pays_id=pays_id)
        if search:
            search_q = build_search_q(search, [
                'titre',
                'summary',
                'notion__titre',
                'notion__theme__matiere__titre',
                'notion__theme__contexte__niveau__nom',
                'notion__theme__contexte__niveau__pays__nom',
            ])
            if search_q:
                qs = qs.filter(search_q)

        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def _apply_limit(self, queryset, request):
        limit = request.query_params.get('limit')
        if not limit:
            return queryset
        try:
            value = int(limit)
        except (TypeError, ValueError):
            return queryset
        if value > 0:
            return queryset[:value]
        return queryset
