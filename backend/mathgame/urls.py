"""URL routes for the Arena game (mounted under /api/arena/)."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ArenaAdminAnalyticsView,
    ArenaAdminChapterViewSet,
    ArenaAdminConfigView,
    ArenaAdminDailyViewSet,
    ArenaAdminLevelViewSet,
    ArenaAdminQuestionViewSet,
    ArenaAttemptHistoryView,
    ArenaChapterViewSet,
    ArenaConfigView,
    ArenaDailyView,
    ArenaForgeView,
    ArenaLevelAttemptView,
    ArenaLevelPlayView,
    ArenaUserStateView,
    ingest_event,
)

# Public-facing player router
player = DefaultRouter()
player.register(r'chapters', ArenaChapterViewSet, basename='arena-chapter')

# Admin router
admin_router = DefaultRouter()
admin_router.register(r'chapters', ArenaAdminChapterViewSet, basename='arena-admin-chapter')
admin_router.register(r'levels', ArenaAdminLevelViewSet, basename='arena-admin-level')
admin_router.register(r'questions', ArenaAdminQuestionViewSet, basename='arena-admin-question')
admin_router.register(r'daily', ArenaAdminDailyViewSet, basename='arena-admin-daily')


urlpatterns = [
    path('config/', ArenaConfigView.as_view(), name='arena-config'),
    path('me/', ArenaUserStateView.as_view(), name='arena-me'),
    path('history/', ArenaAttemptHistoryView.as_view(), name='arena-history'),
    path('daily/', ArenaDailyView.as_view(), name='arena-daily'),
    path('forge/', ArenaForgeView.as_view(), name='arena-forge'),
    path('levels/<int:level_id>/play/', ArenaLevelPlayView.as_view(), name='arena-play'),
    path('levels/<int:level_id>/attempts/', ArenaLevelAttemptView.as_view(), name='arena-attempt'),
    path('events/', ingest_event, name='arena-event'),
    path('', include(player.urls)),

    # Admin
    path('admin/config/', ArenaAdminConfigView.as_view(), name='arena-admin-config'),
    path('admin/analytics/', ArenaAdminAnalyticsView.as_view(), name='arena-admin-analytics'),
    path('admin/', include(admin_router.urls)),
]
