"""
SERIALIZERS ULTRA SIMPLES pour suivis
"""
from rest_framework import serializers
from .models import SuiviExercice, SuiviQuiz, QuizSubmission


class SuiviExerciceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = SuiviExercice
        fields = '__all__'
        read_only_fields = ['user', 'date_creation', 'date_modification']


class SuiviQuizSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = SuiviQuiz
        fields = '__all__'
        read_only_fields = ['user', 'tentative_numero', 'xp_gagne', 'date_creation', 'date_modification']


class QuizSubmissionSerializer(serializers.ModelSerializer):
    """Serializer pour les soumissions manuelles de quiz"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    quiz_titre = serializers.CharField(source='quiz.titre', read_only=True)
    quiz_notion_titre = serializers.CharField(source='quiz.notion.titre', read_only=True)
    corrige_par_email = serializers.EmailField(source='corrige_par.email', read_only=True, allow_null=True)
    
    class Meta:
        model = QuizSubmission
        fields = [
            'id', 'user', 'user_email', 'user_name', 'quiz', 'quiz_titre', 
            'quiz_notion_titre', 'status', 'note', 'commentaire', 
            'corrige_par', 'corrige_par_email', 'date_correction',
            'notes_admin', 'date_creation', 'date_modification'
        ]
        read_only_fields = ['user', 'date_creation', 'date_modification', 'corrige_par', 'date_correction']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()