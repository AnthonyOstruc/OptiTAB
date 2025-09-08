"""
URLs ULTRA SIMPLES pour suivis
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuiviExerciceViewSet, SuiviQuizViewSet, StatusViewSet

router = DefaultRouter()
router.register(r'exercices', SuiviExerciceViewSet)
router.register(r'quiz', SuiviQuizViewSet)
router.register(r'status', StatusViewSet, basename='status')  # Basename unique

urlpatterns = [
    path('', include(router.urls)),
]