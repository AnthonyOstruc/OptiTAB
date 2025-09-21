"""
SERIALIZERS ULTRA SIMPLES pour cours
"""
from rest_framework import serializers
from .models import Cours, CoursImage


class CoursSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cours
        fields = '__all__'

    def get_images(self, obj):
        qs = getattr(obj, 'images', None)
        if qs is None:
            return []
        request = self.context.get('request') if hasattr(self, 'context') else None
        return [
            {
                'id': img.id,
                'image': (
                    request.build_absolute_uri(img.image.url)
                    if request and getattr(img.image, 'url', None)
                    else (img.image.url if getattr(img.image, 'url', None) else '')
                ),
                'image_type': img.image_type,
                'position': img.position,
                'legende': img.legende,
            }
            for img in qs.all().order_by('position', 'id')
        ]


class CoursImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursImage
        fields = '__all__'
        extra_kwargs = {
            'legende': {'required': False, 'allow_blank': True},
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