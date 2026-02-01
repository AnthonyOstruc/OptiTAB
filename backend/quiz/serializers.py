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
    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            request = self.context.get('request') if hasattr(self, 'context') else None
            url = data.get('image')
            # Si l'URL est déjà absolue (S3), ne rien faire
            if url and str(url).startswith(('http://', 'https://')):
                return data
            # Sinon, si on a la requête, construire une URL absolue
            if request and url:
                if str(url).startswith('/'):
                    data['image'] = request.build_absolute_uri(url)
                else:
                    data['image'] = request.build_absolute_uri(f"/media/{url}")
        except Exception:
            pass
        return data
    class Meta:
        model = QuizImage
        fields = '__all__'