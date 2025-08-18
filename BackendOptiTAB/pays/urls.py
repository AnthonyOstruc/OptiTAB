from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaysViewSet, NiveauViewSet

router = DefaultRouter()
router.register(r'pays', PaysViewSet, basename='pays')
router.register(r'niveaux', NiveauViewSet, basename='niveaux')

urlpatterns = [
    path('', include(router.urls)),
]
