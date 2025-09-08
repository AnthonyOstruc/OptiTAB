"""
URLs ULTRA SIMPLES pour exercices
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MatiereViewSet, ThemeViewSet, NotionViewSet,
    ChapitreViewSet, ExerciceViewSet, MatiereContexteViewSet,
    ExerciceImageViewSet
)
# Deprecated legacy endpoints (kept temporarily for compatibility)
from .matiere_pays_views import MatierePaysViewSet, matiere_pays_pour_utilisateur

router = DefaultRouter()
router.register(r'matieres', MatiereViewSet)
router.register(r'contextes', MatiereContexteViewSet, basename='contextes')
router.register(r'themes', ThemeViewSet)
router.register(r'notions', NotionViewSet)
router.register(r'chapitres', ChapitreViewSet)
router.register(r'exercices', ExerciceViewSet)
router.register(r'exercice-images', ExerciceImageViewSet, basename='exercice-image')
# Ancien endpoint déprécié; à supprimer si plus utilisé par le frontend
# router.register(r'matiere-pays', MatierePaysViewSet, basename='matiere-pays')

urlpatterns = [
    path('', include(router.urls)),
    # À terme, à supprimer
    # path('matiere-pays/pour_utilisateur/', matiere_pays_pour_utilisateur, name='matiere_pays_pour_utilisateur'),
]