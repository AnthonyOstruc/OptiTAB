from django.urls import path

from . import views


urlpatterns = [
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
    path('slides/<int:pk>/', views.ReelSlideDetailView.as_view(), name='reel-slide-detail'),
]
