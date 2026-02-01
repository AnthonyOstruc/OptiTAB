from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import update_last_login
from ..models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = (attrs.get('email') or '').strip()
        password = attrs.get('password')

        # Rechercher l'utilisateur sans authentifier deux fois
        try:
            user = CustomUser.objects.get(email__iexact=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Utilisateur introuvable avec cet email.")

        # Vérifier le mot de passe directement pour éviter un double appel à authenticate()
        if not user.check_password(password):
            raise AuthenticationFailed("Mot de passe incorrect.")

        update_last_login(None, user)

        # Générer les tokens directement
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'email_verified': not bool(user.verification_code),
        }
        return data
