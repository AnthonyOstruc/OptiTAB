from rest_framework import serializers
from ..models import CustomUser

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Utilisateur introuvable.')
        if user.verification_code != data['code']:
            raise serializers.ValidationError('Code de vérification incorrect.')
        return data

    def save(self, **kwargs):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.verification_code = None
        user.save()
        return user
