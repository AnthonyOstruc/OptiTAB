"""Arena game API views (player + admin)."""
from datetime import timedelta

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    ArenaAttempt,
    ArenaChapter,
    ArenaConfig,
    ArenaDailyChallenge,
    ArenaEvent,
    ArenaLevel,
    ArenaMistake,
    ArenaQuestion,
    ArenaUserState,
)
from .permissions import ArenaAdminOnly, ArenaVisible, is_admin, is_premium
from .serializers import (
    ArenaAttemptSerializer,
    ArenaChapterAdminSerializer,
    ArenaChapterSerializer,
    ArenaConfigSerializer,
    ArenaDailyChallengeSerializer,
    ArenaEventSerializer,
    ArenaLevelAdminSerializer,
    ArenaLevelSummarySerializer,
    ArenaMistakeSerializer,
    ArenaQuestionAdminSerializer,
    ArenaQuestionPlaySerializer,
    ArenaUserStateSerializer,
)
from .services import can_play_daily, submit_attempt


# --------------------------------------------------------------------------- #
# Public-facing player API
# --------------------------------------------------------------------------- #

class ArenaConfigView(APIView):
    """Public read-only config (so the frontend knows whether to render the game tab)."""
    permission_classes = []

    def get(self, request):
        config = ArenaConfig.get_solo()
        data = ArenaConfigSerializer(config).data
        # Expose admin override flag so the UI can show an "admin preview" badge.
        data['admin_preview'] = is_admin(getattr(request, 'user', None))
        return Response(data)


class ArenaChapterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArenaChapterSerializer
    permission_classes = [IsAuthenticated, ArenaVisible]
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            ArenaChapter.objects.filter(is_active=True)
            .prefetch_related('levels')
            .order_by('order', 'title')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['config'] = ArenaConfig.get_solo()
        return ctx


class ArenaLevelPlayView(APIView):
    """Returns the questions a user is allowed to see for a level."""
    permission_classes = [IsAuthenticated, ArenaVisible]

    def get(self, request, level_id: int):
        try:
            level = ArenaLevel.objects.select_related('chapter').get(pk=level_id, is_active=True)
        except ArenaLevel.DoesNotExist:
            return Response({'detail': 'Niveau introuvable.'}, status=404)

        config = ArenaConfig.get_solo()
        # Free-tier soft lock: levels beyond the free quota require premium.
        if not is_premium(request.user) and level.order > config.free_levels_per_chapter:
            return Response(
                {
                    'detail': 'Niveau réservé aux abonnés.',
                    'cta': {
                        'id': 'unlock_level',
                        'title': "Niveau premium",
                        'body': "Continuez votre progression avec OptiTAB+.",
                        'cta': "Voir l'offre",
                        'route': '/tarifs',
                        'trigger': 'level_locked',
                    },
                },
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )
        if level.is_premium and not is_premium(request.user):
            return Response(
                {
                    'detail': 'Niveau Élite réservé aux abonnés.',
                    'cta': {
                        'id': 'unlock_elite',
                        'title': "Niveau Élite",
                        'body': "Accédez aux niveaux avancés et à l'entraînement illimité.",
                        'cta': "Activer OptiTAB+",
                        'route': '/tarifs',
                        'trigger': 'elite_locked_view',
                    },
                },
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        questions = level.questions.all().order_by('order')
        data = ArenaQuestionPlaySerializer(questions, many=True, context={'request': request}).data
        ArenaEvent.objects.create(
            user=request.user, name='level_started',
            payload={'level_id': level.id, 'chapter_id': level.chapter_id},
        )
        return Response({
            'level': ArenaLevelSummarySerializer(
                level, context={'request': request, 'config': config},
            ).data,
            'questions': data,
        })


class ArenaLevelAttemptView(APIView):
    """Submit a played attempt and receive score + CTAs."""
    permission_classes = [IsAuthenticated, ArenaVisible]

    def post(self, request, level_id: int):
        try:
            level = ArenaLevel.objects.get(pk=level_id, is_active=True)
        except ArenaLevel.DoesNotExist:
            return Response({'detail': 'Niveau introuvable.'}, status=404)

        if level.is_premium and not is_premium(request.user):
            return Response({'detail': 'Niveau réservé aux abonnés.'}, status=402)

        result = submit_attempt(
            user=request.user,
            level=level,
            answers=request.data.get('answers') or [],
            duration_sec=request.data.get('duration_sec') or 0,
            used_hint=bool(request.data.get('used_hint')),
            is_daily=bool(request.data.get('is_daily')),
        )
        ArenaEvent.objects.create(
            user=request.user,
            name='level_completed' if result['passed'] else 'level_failed',
            payload={'level_id': level.id, 'score': result['score'], 'accuracy': result['accuracy']},
        )
        return Response(result)


class ArenaDailyView(APIView):
    """Get today's daily challenge."""
    permission_classes = [IsAuthenticated, ArenaVisible]

    def get(self, request):
        today = timezone.localdate()
        daily = (
            ArenaDailyChallenge.objects
            .select_related('level', 'level__chapter')
            .filter(date=today)
            .first()
        )
        if not daily:
            return Response({'available': False, 'message': "Aucun défi quotidien aujourd'hui."})

        playable, reason = can_play_daily(request.user, today)
        payload = {
            'available': True,
            'daily': ArenaDailyChallengeSerializer(daily).data,
            'playable': playable,
            'reason': reason,
        }
        if not playable:
            payload['cta'] = {
                'id': 'daily_replay',
                'title': "Encore envie de jouer ?",
                'body': "Avec OptiTAB+, le défi quotidien est rejouable autant de fois que vous le souhaitez.",
                'cta': "Activer OptiTAB+",
                'route': '/tarifs',
                'trigger': 'daily_limit_reached',
            }
        return Response(payload)


class ArenaForgeView(APIView):
    """Mistake forge — review past mistakes (truncated for free users)."""
    permission_classes = [IsAuthenticated, ArenaVisible]

    def get(self, request):
        qs = (
            ArenaMistake.objects
            .filter(user=request.user)
            .select_related('question', 'question__level', 'question__level__chapter')
            .order_by('-last_seen')
        )
        free_limit = 5
        truncated = False
        if not is_premium(request.user):
            total = qs.count()
            qs = qs[:free_limit]
            truncated = total > free_limit
        data = ArenaMistakeSerializer(qs, many=True).data
        payload = {'mistakes': data, 'truncated': truncated}
        if truncated:
            payload['cta'] = {
                'id': 'forge_unlimited',
                'title': "Voir toutes vos erreurs",
                'body': "OptiTAB+ enregistre l'historique complet de la Forge et active la révision intelligente.",
                'cta': "Découvrir OptiTAB+",
                'route': '/tarifs',
                'trigger': 'forge_truncated',
            }
        return Response(payload)


class ArenaUserStateView(APIView):
    """Current user state (XP, streak, etc.)."""
    permission_classes = [IsAuthenticated, ArenaVisible]

    def get(self, request):
        state, _ = ArenaUserState.objects.get_or_create(user=request.user)
        return Response({
            'state': ArenaUserStateSerializer(state).data,
            'is_premium': is_premium(request.user),
            'is_admin': is_admin(request.user),
            'user_xp': getattr(request.user, 'xp', 0),
        })


class ArenaAttemptHistoryView(APIView):
    permission_classes = [IsAuthenticated, ArenaVisible]

    def get(self, request):
        qs = (
            ArenaAttempt.objects
            .filter(user=request.user)
            .order_by('-created_at')[:50]
        )
        return Response(ArenaAttemptSerializer(qs, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ArenaVisible])
def ingest_event(request):
    """Lightweight analytics ingest from the frontend."""
    name = (request.data.get('name') or '').strip()[:80]
    if not name:
        return Response({'detail': 'name requis'}, status=400)
    payload = request.data.get('payload') or {}
    if not isinstance(payload, dict):
        payload = {'value': payload}
    event = ArenaEvent.objects.create(user=request.user, name=name, payload=payload)
    return Response(ArenaEventSerializer(event).data, status=201)


# --------------------------------------------------------------------------- #
# Admin API
# --------------------------------------------------------------------------- #

class ArenaAdminConfigView(APIView):
    permission_classes = [IsAuthenticated, ArenaAdminOnly]

    def get(self, request):
        return Response(ArenaConfigSerializer(ArenaConfig.get_solo()).data)

    def patch(self, request):
        config = ArenaConfig.get_solo()
        serializer = ArenaConfigSerializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ArenaAdminChapterViewSet(viewsets.ModelViewSet):
    queryset = ArenaChapter.objects.all().order_by('order', 'title')
    serializer_class = ArenaChapterAdminSerializer
    permission_classes = [IsAuthenticated, ArenaAdminOnly]


class ArenaAdminLevelViewSet(viewsets.ModelViewSet):
    queryset = ArenaLevel.objects.all().order_by('chapter', 'order')
    serializer_class = ArenaLevelAdminSerializer
    permission_classes = [IsAuthenticated, ArenaAdminOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        chapter_id = self.request.query_params.get('chapter')
        if chapter_id:
            qs = qs.filter(chapter_id=chapter_id)
        return qs


class ArenaAdminQuestionViewSet(viewsets.ModelViewSet):
    queryset = ArenaQuestion.objects.all().order_by('level', 'order')
    serializer_class = ArenaQuestionAdminSerializer
    permission_classes = [IsAuthenticated, ArenaAdminOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        level_id = self.request.query_params.get('level')
        if level_id:
            qs = qs.filter(level_id=level_id)
        return qs


class ArenaAdminDailyViewSet(viewsets.ModelViewSet):
    queryset = ArenaDailyChallenge.objects.all().select_related('level').order_by('-date')
    serializer_class = ArenaDailyChallengeSerializer
    permission_classes = [IsAuthenticated, ArenaAdminOnly]


class ArenaAdminAnalyticsView(APIView):
    """Aggregate KPIs for the admin dashboard."""
    permission_classes = [IsAuthenticated, ArenaAdminOnly]

    def get(self, request):
        from django.db.models import Avg, Count
        events_qs = ArenaEvent.objects.values('name').annotate(count=Count('id')).order_by('-count')
        attempts = ArenaAttempt.objects.aggregate(
            total=Count('id'),
            avg_accuracy=Avg('accuracy'),
            avg_xp=Avg('xp_awarded'),
        )
        cutoff_30d = timezone.now() - timedelta(days=30)
        # Content readiness — lets the admin gauge whether the game is ready
        # to flip is_public, without leaving the dashboard.
        active_questions = ArenaQuestion.objects.filter(level__is_active=True).count()
        content = {
            'chapters': ArenaChapter.objects.count(),
            'chapters_active': ArenaChapter.objects.filter(is_active=True).count(),
            'levels': ArenaLevel.objects.count(),
            'levels_active': ArenaLevel.objects.filter(is_active=True).count(),
            'questions': ArenaQuestion.objects.count(),
            'questions_active': active_questions,
            'daily_scheduled': ArenaDailyChallenge.objects
                .filter(date__gte=timezone.localdate()).count(),
            'daily_today': ArenaDailyChallenge.objects
                .filter(date=timezone.localdate()).count(),
        }
        # Conversion funnel for the last 30 days. Counts only events that the
        # frontend actually emits (game_started, level_started, level_completed,
        # cta_displayed, cta_clicked, cta_dismissed). Click-through rate is
        # derived client-side so the shape stays minimal.
        funnel_names = [
            'game_started', 'level_started', 'level_completed', 'level_failed',
            'cta_displayed', 'cta_clicked', 'cta_dismissed',
            'forge_opened', 'hint_used',
        ]
        funnel_counts = dict.fromkeys(funnel_names, 0)
        for row in (
            ArenaEvent.objects
            .filter(created_at__gte=cutoff_30d, name__in=funnel_names)
            .values('name').annotate(count=Count('id'))
        ):
            funnel_counts[row['name']] = row['count']
        return Response({
            'events_by_name': list(events_qs),
            'attempts': attempts,
            'unique_players_30d': ArenaAttempt.objects
                .filter(created_at__gte=cutoff_30d)
                .values('user_id').distinct().count(),
            'content': content,
            'funnel_30d': funnel_counts,
        })
