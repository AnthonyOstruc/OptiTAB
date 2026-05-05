"""Serializers for the Arena game API."""
from rest_framework import serializers

from .models import (
    ArenaAnswer,
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
from .permissions import is_premium


class ArenaConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaConfig
        fields = [
            'is_public',
            'daily_xp_bonus',
            'streak_shield_enabled',
            'free_levels_per_chapter',
            'free_hints_per_day',
            'version',
            'updated_at',
        ]


class ArenaQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaQuestion
        fields = '__all__'


class ArenaQuestionPlaySerializer(serializers.ModelSerializer):
    """
    Serializer used during play.

    - Strips `correct` (validated server-side only).
    - Hides `hint` and `explanation` for non-premium users.
    """
    explanation = serializers.SerializerMethodField()
    hint = serializers.SerializerMethodField()

    class Meta:
        model = ArenaQuestion
        fields = ['id', 'order', 'type', 'prompt', 'choices', 'hint', 'explanation', 'weight']

    def _premium(self):
        request = self.context.get('request')
        return is_premium(getattr(request, 'user', None))

    def get_explanation(self, obj):
        text = obj.explanation or ''
        if not text:
            return ''
        if self._premium():
            return text
        # Free users see a teaser only.
        teaser = text.strip().split('\n', 1)[0][:120]
        return teaser + ('… 🔒' if len(text) > len(teaser) else '')

    def get_hint(self, obj):
        if self._premium():
            return obj.hint or ''
        return ''


class ArenaLevelSummarySerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)
    locked = serializers.SerializerMethodField()

    class Meta:
        model = ArenaLevel
        fields = [
            'id', 'title', 'order', 'difficulty',
            'time_limit_sec', 'xp_reward', 'pass_threshold',
            'is_premium', 'questions_count', 'locked',
        ]

    def get_locked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if obj.is_premium and not is_premium(user):
            return True
        # Free tier limits the number of accessible levels per chapter.
        config = self.context.get('config') or ArenaConfig.get_solo()
        if not is_premium(user) and obj.order > config.free_levels_per_chapter:
            return True
        return False


class ArenaChapterSerializer(serializers.ModelSerializer):
    levels = ArenaLevelSummarySerializer(many=True, read_only=True)
    locked = serializers.SerializerMethodField()

    class Meta:
        model = ArenaChapter
        fields = [
            'id', 'title', 'slug', 'description', 'icon',
            'color', 'order', 'is_premium', 'is_active', 'levels', 'locked',
        ]

    def get_locked(self, obj):
        if not obj.is_premium:
            return False
        request = self.context.get('request')
        return not is_premium(getattr(request, 'user', None))


class ArenaChapterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaChapter
        fields = '__all__'


class ArenaLevelAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaLevel
        fields = '__all__'


class ArenaDailyChallengeSerializer(serializers.ModelSerializer):
    level = ArenaLevelSummarySerializer(read_only=True)
    level_id = serializers.PrimaryKeyRelatedField(
        queryset=ArenaLevel.objects.all(), source='level', write_only=True,
    )

    class Meta:
        model = ArenaDailyChallenge
        fields = ['id', 'date', 'bonus_xp', 'level', 'level_id']


class ArenaUserStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaUserState
        fields = [
            'current_streak', 'best_streak', 'last_played_date',
            'streak_shields_used', 'daily_hints_used',
            'total_levels_completed', 'total_xp_earned',
            'last_daily_completed_date',
        ]


class ArenaAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaAttempt
        fields = [
            'id', 'level', 'score', 'max_score', 'accuracy',
            'duration_sec', 'used_hint', 'is_daily', 'passed',
            'xp_awarded', 'created_at',
        ]
        read_only_fields = fields


class ArenaAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaAnswer
        fields = ['question', 'user_answer', 'is_correct', 'time_ms']


class ArenaMistakeSerializer(serializers.ModelSerializer):
    question_prompt = serializers.CharField(source='question.prompt', read_only=True)
    chapter_title = serializers.CharField(source='question.level.chapter.title', read_only=True)
    level_title = serializers.CharField(source='question.level.title', read_only=True)

    class Meta:
        model = ArenaMistake
        fields = [
            'id', 'question', 'question_prompt', 'chapter_title',
            'level_title', 'last_seen', 'times_wrong', 'mastery',
        ]


class ArenaEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArenaEvent
        fields = ['id', 'name', 'payload', 'created_at']
        read_only_fields = ['id', 'created_at']
