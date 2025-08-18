"""
URLs ULTRA SIMPLES pour cours
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoursViewSet

router = DefaultRouter()
router.register(r'cours', CoursViewSet)

urlpatterns = [
    path('', include(router.urls)),
]