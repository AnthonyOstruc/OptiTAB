"""
VUES ULTRA SIMPLES pour quiz
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Quiz, QuizImage
from .serializers import QuizSerializer, QuizImageSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée

    def get_queryset(self):
        queryset = super().get_queryset()
        chapitre = self.request.query_params.get('chapitre')
        
        if chapitre:
            queryset = queryset.filter(chapitre_id=chapitre)
            
        return queryset.filter(est_actif=True)


class QuizImageViewSet(viewsets.ModelViewSet):
    """CRUD pour les images de quiz
    
    Frontend attends /api/quiz-images/ avec filtre ?quiz=<id>
    """
    queryset = QuizImage.objects.all()
    serializer_class = QuizImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        quiz_id = self.request.query_params.get('quiz')
        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)
        return queryset.order_by('position', 'id')