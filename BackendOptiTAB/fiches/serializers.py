"""
SERIALIZERS ULTRA SIMPLES pour fiches
"""
from rest_framework import serializers
from .models import FicheSynthese


class FicheSyntheseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheSynthese
        fields = '__all__'