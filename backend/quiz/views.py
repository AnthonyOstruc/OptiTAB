"""
VUES ULTRA SIMPLES pour quiz
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from subscriptions.permissions import (
    HasActiveSubscriptionOrPass,
)
from .models import Quiz, QuizImage
from subscriptions.acces_contenu import ContenuMixin, EcritureAdminMixin, vide
from .serializers import QuizSerializer, QuizImageSerializer


class QuizViewSet(EcritureAdminMixin, ContenuMixin, viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    champs_payants = {'questions_data': vide, 'solution': ''}
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasActiveSubscriptionOrPass()]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Nouveau filtrage direct par notion (suppression des chapitres)
        notion = self.request.query_params.get('notion')
        matiere = self.request.query_params.get('matiere')
        search = self.request.query_params.get('search') or self.request.query_params.get('q')

        if notion:
            queryset = queryset.filter(notion_id=notion)
        if matiere:
            queryset = queryset.select_related('notion', 'notion__theme', 'notion__theme__matiere')
            queryset = queryset.filter(notion__theme__matiere_id=matiere)

        if search:
            queryset = queryset.filter(titre__icontains=search)

        return (
            queryset
            .select_related('notion', 'notion__theme', 'notion__theme__matiere')
            .filter(est_actif=True)
            .order_by('notion_id', 'titre', 'id')
        )


class QuizImageViewSet(EcritureAdminMixin, viewsets.ModelViewSet):
    """CRUD pour les images de quiz
    
    Frontend attends /api/quiz-images/ avec filtre ?quiz=<id>
    """
    queryset = QuizImage.objects.all()
    serializer_class = QuizImageSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_queryset(self):
        queryset = super().get_queryset()
        quiz_id = self.request.query_params.get('quiz')
        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)
        return queryset.order_by('position', 'id')
