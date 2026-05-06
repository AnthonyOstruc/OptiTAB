from django.urls import path

from . import views


urlpatterns = [
    path('voices/', views.ReelVoiceListView.as_view(), name='reel-voice-list'),
    path('voices/library/', views.ReelVoiceLibraryView.as_view(), name='reel-voice-library'),
    path('test-voice/', views.ReelTTSTestVoiceView.as_view(), name='reel-tts-test-voice'),
    path('projects/', views.ReelProjectListCreateView.as_view(), name='reel-project-list-create'),
    path('projects/<int:pk>/', views.ReelProjectDetailView.as_view(), name='reel-project-detail'),
    path(
        'projects/<int:pk>/generate-demo-slides/',
        views.ReelProjectGenerateDemoSlidesView.as_view(),
        name='reel-project-generate-demo-slides',
    ),
    path(
        'projects/<int:pk>/generate-from-template/',
        views.ReelProjectGenerateFromTemplateView.as_view(),
        name='reel-project-generate-from-template',
    ),
    path(
        'projects/<int:pk>/save-template/',
        views.ReelProjectSaveTemplateView.as_view(),
        name='reel-project-save-template',
    ),
    path(
        'projects/<int:pk>/generate-speech/',
        views.ReelProjectGenerateSpeechView.as_view(),
        name='reel-project-generate-speech',
    ),
    path(
        'projects/<int:pk>/generate-slide-speeches/',
        views.ReelProjectGenerateSlideSpeechesView.as_view(),
        name='reel-project-generate-slide-speeches',
    ),
    path(
        'projects/<int:pk>/export-video/',
        views.ReelProjectExportVideoView.as_view(),
        name='reel-project-export-video',
    ),
    path(
        'projects/<int:pk>/download-video/',
        views.ReelProjectDownloadVideoView.as_view(),
        name='reel-project-download-video',
    ),
    path(
        'slides/<int:pk>/generate-speech/',
        views.ReelSlideGenerateSpeechView.as_view(),
        name='reel-slide-generate-speech',
    ),
    path('slides/<int:pk>/', views.ReelSlideDetailView.as_view(), name='reel-slide-detail'),
]
