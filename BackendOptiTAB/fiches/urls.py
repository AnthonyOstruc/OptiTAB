"""
URLs ULTRA SIMPLES pour fiches
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FicheSyntheseViewSet

router = DefaultRouter()
router.register(r'fiches', FicheSyntheseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]