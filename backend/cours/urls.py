"""
URLs ULTRA SIMPLES pour cours
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoursViewSet, CoursImageViewSet

router = DefaultRouter()
router.register(r'cours', CoursViewSet)
router.register(r'cours-images', CoursImageViewSet, basename='cours-image')

urlpatterns = [
    path('', include(router.urls)),
]