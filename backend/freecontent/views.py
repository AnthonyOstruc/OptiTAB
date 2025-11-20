from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from cours.models import Cours
from curriculum.models import Exercice
from synthesis.models import SynthesisSheet
from .models import FreeLearningResource
from .serializers import (
    FreeLearningResourceSerializer,
    CourseFreePreviewSerializer,
    ExerciceFreePreviewSerializer,
    SynthesisFreePreviewSerializer
)


class FreeLearningResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API publique pour lister les ressources gratuites (cours, resumes, exercices).

    Aucun jeton requis : ces ressources servent a rassurer avant abonnement.
    """

    serializer_class = FreeLearningResourceSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
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
            qs = qs.filter(
                Q(titre__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(accroche__icontains=search) |
                Q(contenu_html__icontains=search)
            )

        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def list(self, request, *args, **kwargs):
        resource_type = request.query_params.get('type') or request.query_params.get('resource_type')

        if resource_type == FreeLearningResource.TYPE_COURSE:
            queryset = self._apply_limit(self._get_free_courses_queryset(request), request)
            serializer = CourseFreePreviewSerializer(queryset, many=True, context=self.get_serializer_context())
            return Response(serializer.data)
        if resource_type == FreeLearningResource.TYPE_EXERCISE:
            queryset = self._apply_limit(self._get_free_exercises_queryset(request), request)
            serializer = ExerciceFreePreviewSerializer(queryset, many=True, context=self.get_serializer_context())
            return Response(serializer.data)
        if resource_type == FreeLearningResource.TYPE_SUMMARY:
            queryset = self._apply_limit(self._get_free_summaries_queryset(request), request)
            serializer = SynthesisFreePreviewSerializer(queryset, many=True, context=self.get_serializer_context())
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = self._apply_limit(queryset, request)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get(self.lookup_field)
        if slug and slug.startswith('cours-gratuit-'):
            try:
                course_id = int(slug.replace('cours-gratuit-', ''))
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
                exercice_id = int(slug.replace('exercice-gratuit-', ''))
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
                sheet_id = int(slug.replace('synthese-gratuite-', ''))
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
            .order_by('ordre', 'notion__titre')
        )

        params = request.query_params
        matiere_id = params.get('matiere')
        niveau_id = params.get('niveau')
        notion_id = params.get('notion')
        pays_id = params.get('pays')
        search = params.get('q')

        if matiere_id:
            qs = qs.filter(notion__theme__matiere_id=matiere_id)
        if niveau_id:
            qs = qs.filter(notion__theme__contexte__niveau_id=niveau_id)
        if notion_id:
            qs = qs.filter(notion_id=notion_id)
        if pays_id:
            qs = qs.filter(notion__theme__contexte__niveau__pays_id=pays_id)
        if search:
            qs = qs.filter(
                Q(titre__icontains=search) |
                Q(contenu__icontains=search) |
                Q(notion__titre__icontains=search) |
                Q(notion__theme__matiere__titre__icontains=search)
            )

        ordering = params.get('ordering')
        if ordering:
            qs = qs.order_by(ordering)

        return qs

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
            .order_by('ordre', 'notion__titre')
        )

        params = request.query_params
        matiere_id = params.get('matiere')
        niveau_id = params.get('niveau')
        notion_id = params.get('notion')
        pays_id = params.get('pays')
        search = params.get('q')

        if matiere_id:
            qs = qs.filter(notion__theme__matiere_id=matiere_id)
        if niveau_id:
            qs = qs.filter(notion__theme__contexte__niveau_id=niveau_id)
        if notion_id:
            qs = qs.filter(notion_id=notion_id)
        if pays_id:
            qs = qs.filter(notion__theme__contexte__niveau__pays_id=pays_id)
        if search:
            qs = qs.filter(
                Q(titre__icontains=search) |
                Q(contenu__icontains=search) |
                Q(question__icontains=search) |
                Q(notion__titre__icontains=search) |
                Q(notion__theme__matiere__titre__icontains=search)
            )

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
            .order_by('ordre', 'notion__titre')
        )

        params = request.query_params
        matiere_id = params.get('matiere')
        niveau_id = params.get('niveau')
        notion_id = params.get('notion')
        pays_id = params.get('pays')
        search = params.get('q')

        if matiere_id:
            qs = qs.filter(notion__theme__matiere_id=matiere_id)
        if niveau_id:
            qs = qs.filter(notion__theme__contexte__niveau_id=niveau_id)
        if notion_id:
            qs = qs.filter(notion_id=notion_id)
        if pays_id:
            qs = qs.filter(notion__theme__contexte__niveau__pays_id=pays_id)
        if search:
            qs = qs.filter(
                Q(titre__icontains=search) |
                Q(summary__icontains=search) |
                Q(notion__titre__icontains=search) |
                Q(notion__theme__matiere__titre__icontains=search)
            )

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
