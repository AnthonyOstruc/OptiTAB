"""
URLs ULTRA SIMPLES pour quiz
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuizImageViewSet

router = DefaultRouter()
router.register(r'quiz', QuizViewSet)
router.register(r'quiz-images', QuizImageViewSet, basename='quiz-image')

urlpatterns = [
    path('', include(router.urls)),
]