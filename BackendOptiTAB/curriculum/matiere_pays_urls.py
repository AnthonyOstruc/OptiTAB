"""
URLs pour les matières par pays
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .matiere_pays_views import MatierePaysViewSet, matiere_pays_pour_utilisateur

router = DefaultRouter()
router.register(r'matiere-pays', MatierePaysViewSet, basename='matiere-pays')

urlpatterns = [
    path('', include(router.urls)),
    # Alternative endpoint direct
    path('matiere-pays/pour_utilisateur/', matiere_pays_pour_utilisateur, name='matiere_pays_pour_utilisateur'),
]
