"""
SERIALIZERS ULTRA SIMPLES pour quiz
"""
from rest_framework import serializers
from .models import Quiz, QuizImage


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizImageSerializer(serializers.ModelSerializer):
    """Serializer pour les images de quiz"""
    class Meta:
        model = QuizImage
        fields = '__all__'