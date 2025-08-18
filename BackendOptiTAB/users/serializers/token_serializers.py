from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from ..models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Utilisateur introuvable avec cet email.")
        user = authenticate(username=user.email, password=password)
        if not user:
            raise AuthenticationFailed("Mot de passe incorrect.")
        data = super().validate(attrs)
        data['user_id'] = user.id
        data['email'] = user.email
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['is_staff'] = user.is_staff
        return data
