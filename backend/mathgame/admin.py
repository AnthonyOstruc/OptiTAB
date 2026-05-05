"""Django admin registration for the Arena game."""
from django.contrib import admin

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


@admin.register(ArenaConfig)
class ArenaConfigAdmin(admin.ModelAdmin):
    list_display = ['version', 'is_public', 'free_levels_per_chapter', 'updated_at']

    def has_add_permission(self, request):
        return not ArenaConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class ArenaLevelInline(admin.TabularInline):
    model = ArenaLevel
    extra = 0
    fields = ('order', 'title', 'difficulty', 'is_premium', 'time_limit_sec', 'xp_reward', 'is_active')


@admin.register(ArenaChapter)
class ArenaChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order', 'is_premium', 'is_active']
    list_filter = ['is_premium', 'is_active']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArenaLevelInline]


class ArenaQuestionInline(admin.StackedInline):
    model = ArenaQuestion
    extra = 0


@admin.register(ArenaLevel)
class ArenaLevelAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'order', 'title', 'difficulty', 'is_premium', 'is_active']
    list_filter = ['difficulty', 'is_premium', 'is_active']
    inlines = [ArenaQuestionInline]


@admin.register(ArenaQuestion)
class ArenaQuestionAdmin(admin.ModelAdmin):
    list_display = ['level', 'order', 'type', 'weight']
    list_filter = ['type']


@admin.register(ArenaDailyChallenge)
class ArenaDailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['date', 'level', 'bonus_xp']
    date_hierarchy = 'date'


@admin.register(ArenaUserState)
class ArenaUserStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'best_streak', 'total_xp_earned', 'last_played_date']
    search_fields = ['user__email']


@admin.register(ArenaAttempt)
class ArenaAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'score', 'max_score', 'accuracy', 'passed', 'is_daily', 'created_at']
    list_filter = ['passed', 'is_daily']
    search_fields = ['user__email', 'level__title']


@admin.register(ArenaMistake)
class ArenaMistakeAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'mastery', 'times_wrong', 'last_seen']
    search_fields = ['user__email']


@admin.register(ArenaEvent)
class ArenaEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['name']
    date_hierarchy = 'created_at'
