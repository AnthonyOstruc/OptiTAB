from rest_framework import serializers

from curriculum.serializers import NotionSerializer
from .models import SynthesisImage, SynthesisSheet
from .utils import build_synthesis_image_payload, resolve_synthesis_title


class SynthesisSheetSerializer(serializers.ModelSerializer):
    notion_info = NotionSerializer(source='notion', read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SynthesisSheet
        fields = [
            'id', 'titre', 'notion', 'notion_info', 'summary',
            'key_points', 'formulas', 'examples',
            'reading_time_minutes', 'access_scope', 'sheet_type',
            'est_actif', 'date_creation', 'date_modification', 'images'
        ]
        read_only_fields = ['date_creation', 'date_modification']

    def validate(self, data):
        if not data.get('summary'):
            raise serializers.ValidationError("Le champ 'summary' doit etre rempli")
        return data

    def get_images(self, obj):
        qs = getattr(obj, 'images', None)
        if qs is None:
            return []

        request = self.context.get('request') if hasattr(self, 'context') else None
        synthesis_title = resolve_synthesis_title(obj)
        return [
            build_synthesis_image_payload(
                img,
                request=request,
                synthesis_title=synthesis_title
            )
            for img in qs.all().order_by('position', 'id')
        ]


class SynthesisSheetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisSheet
        fields = [
            'titre', 'notion', 'summary', 'key_points',
            'formulas', 'examples', 'reading_time_minutes', 'access_scope', 'sheet_type'
        ]


class SynthesisImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisImage
        fields = '__all__'
        extra_kwargs = {
            'caption': {'required': False, 'allow_blank': True},
            'position': {'required': False},
            'alt_text': {'required': False, 'allow_blank': True},
            'title_text': {'required': False, 'allow_blank': True},
            'width': {'required': False},
            'height': {'required': False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request') if hasattr(self, 'context') else None
        synthesis_title = resolve_synthesis_title(getattr(instance, 'sheet', None))
        payload = build_synthesis_image_payload(
            instance,
            request=request,
            synthesis_title=synthesis_title
        )

        data['image'] = payload['image']
        data['caption'] = payload['caption']
        data['legende'] = payload['legende']
        data['alt_text_resolved'] = payload['alt_text_resolved']
        data['title_text_resolved'] = payload['title_text_resolved']
        data['width'] = payload['width']
        data['height'] = payload['height']
        return data


class SynthesisSheetListSerializer(serializers.ModelSerializer):
    notion_nom = serializers.CharField(source='notion.titre', read_only=True)
    theme_nom = serializers.CharField(source='notion.theme.titre', read_only=True)
    matiere_nom = serializers.CharField(source='notion.theme.matiere.titre', read_only=True)

    class Meta:
        model = SynthesisSheet
        fields = [
            'id', 'titre', 'notion', 'notion_nom',
            'theme_nom', 'matiere_nom', 'reading_time_minutes',
            'access_scope', 'sheet_type', 'est_actif', 'date_creation', 'summary'
        ]
