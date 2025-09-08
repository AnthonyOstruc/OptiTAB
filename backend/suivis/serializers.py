"""
SERIALIZERS ULTRA SIMPLES pour suivis
"""
from rest_framework import serializers
from .models import SuiviExercice, SuiviQuiz


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