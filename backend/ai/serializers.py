from rest_framework import serializers
from .models import AIConversation


class AIConversationSerializer(serializers.ModelSerializer):
    """Serializer pour les conversations IA"""

    class Meta:
        model = AIConversation
        fields = [
            'id', 'user', 'message', 'ai_response',
            'contexte_matiere', 'contexte_chapitre',
            'tokens_used', 'model_used', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'ai_response', 'tokens_used', 'created_at']


class AIQuerySerializer(serializers.Serializer):
    """Serializer pour les requêtes IA"""
    message = serializers.CharField(required=True)
    matiere_contexte_id = serializers.IntegerField(required=False, allow_null=True)
    chapitre_id = serializers.IntegerField(required=False, allow_null=True)
    model = serializers.ChoiceField(choices=['gpt-3.5-turbo', 'gpt-4'], default='gpt-3.5-turbo', required=False)
