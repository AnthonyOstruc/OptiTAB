from rest_framework import serializers
from .models import SynthesisSheet
from curriculum.serializers import NotionSerializer


class SynthesisSheetSerializer(serializers.ModelSerializer):
    notion_info = NotionSerializer(source='notion', read_only=True)
    
    class Meta:
        model = SynthesisSheet
        fields = [
            'id', 'titre', 'notion', 'notion_info', 'summary',
            'key_points', 'formulas', 'examples', 'difficulty', 'ordre',
            'reading_time_minutes', 'est_actif', 'date_creation', 'date_modification'
        ]
        read_only_fields = ['date_creation', 'date_modification']

    def validate(self, data):
        """Validation personnalisée"""
        if not data.get('summary'):
            raise serializers.ValidationError(
                "Le champ 'summary' doit être rempli"
            )
        return data


class SynthesisSheetCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour la création"""
    
    class Meta:
        model = SynthesisSheet
        fields = [
            'titre', 'notion', 'summary', 'key_points', 
            'formulas', 'examples', 'difficulty', 'ordre', 'reading_time_minutes'
        ]


class SynthesisSheetListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la liste (plus léger)"""
    notion_nom = serializers.CharField(source='notion.titre', read_only=True)
    theme_nom = serializers.CharField(source='notion.theme.titre', read_only=True)
    matiere_nom = serializers.CharField(source='notion.theme.matiere.titre', read_only=True)
    
    class Meta:
        model = SynthesisSheet
        fields = [
            'id', 'titre', 'notion', 'notion_nom', 
            'theme_nom', 'matiere_nom', 'difficulty', 'reading_time_minutes',
            'est_actif', 'date_creation', 'ordre', 'summary'
        ]
