from rest_framework import serializers
from .models import SynthesisSheet, SynthesisImage
from curriculum.serializers import NotionSerializer


class SynthesisSheetSerializer(serializers.ModelSerializer):
    notion_info = NotionSerializer(source='notion', read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = SynthesisSheet
        fields = [
            'id', 'titre', 'notion', 'notion_info', 'summary',
            'key_points', 'formulas', 'examples', 'difficulty', 'ordre',
            'reading_time_minutes', 'est_actif', 'date_creation', 'date_modification', 'images'
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


class SynthesisImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisImage
        fields = '__all__'
        extra_kwargs = {
            'caption': {'required': False, 'allow_blank': True},
            'position': {'required': False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            request = self.context.get('request') if hasattr(self, 'context') else None
            if request and data.get('image') and not str(data['image']).startswith('http'):
                data['image'] = request.build_absolute_uri(data['image'])
        except Exception:
            pass
        return data


    
def get_images(self, obj):
    qs = getattr(obj, 'images', None)
    if qs is None:
        return []
    request = self.context.get('request') if hasattr(self, 'context') else None
    return [
        {
            'id': img.id,
            'image': (
                img.image.url if (getattr(img.image, 'url', None) and str(img.image.url).startswith(('http://', 'https://')))
                else (
                    request.build_absolute_uri(img.image.url) if (request and getattr(img.image, 'url', None)) else (img.image.url if getattr(img.image, 'url', None) else '')
                )
            ),
            'image_type': img.image_type,
            'position': img.position,
            'caption': img.caption,
        }
        for img in qs.all().order_by('position', 'id')
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
