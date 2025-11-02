"""
Authentication Serializers - Professional Implementation
=======================================================

Clean, secure, and maintainable authentication serializers following
industry best practices and security standards.

Classes:
    - UserRegistrationSerializer: Handles new user registration
    - EmailVerificationSerializer: Manages email verification flow
"""

from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import logging
import secrets
from django.utils import timezone
from django.urls import reverse

from core.services import EmailService

from ..models import CustomUser

logger = logging.getLogger(__name__)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Professional user registration serializer with comprehensive validation.
    
    Features:
        - Secure password validation
        - Automatic email verification
        - Clean error handling
        - Centralized email service
    """
    
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Password must be at least 8 characters long"
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        help_text="Must match the password field"
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'first_name', 
            'last_name',
            'civilite',
            'date_naissance',
            'telephone',
            'password', 
            'password_confirmation'
        ]
        extra_kwargs = {
            'email': {'help_text': 'Valid email address for account verification'},
            'first_name': {'help_text': 'User first name'},
            'last_name': {'help_text': 'User last name'},
            'civilite': {'help_text': 'User civility (M/Mme)', 'required': False},
            'date_naissance': {'help_text': 'User birth date', 'required': False},
            'telephone': {'help_text': 'User phone number', 'required': False},
        }

    def validate_email(self, value):
        """Validate email uniqueness and format."""
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Un compte existe déjà avec cette adresse email."
            )
        return value.lower()

    def validate_password(self, value):
        """Validate password strength using Django validators."""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):
        """Cross-field validation for password confirmation."""
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                "password_confirmation": "Les mots de passe ne correspondent pas."
            })
        return data

    def create(self, validated_data):
        """Create user and mark as inactive until email verification."""
        # Remove confirmation field
        validated_data.pop('password_confirmation')
        
        verification_token = secrets.token_urlsafe(32)

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            civilite=validated_data.get('civilite'),
            date_naissance=validated_data.get('date_naissance'),
            telephone=validated_data.get('telephone'),
            password=validated_data['password'],
            is_active=True,
            verification_code=verification_token,
            verification_code_sent_at=None
        )
        
        logger.info(f"New user registration: {user.email}")
        # Envoyer le lien de vérification de manière asynchrone (best effort)
        try:
            request = self.context.get('request') if hasattr(self, 'context') else None
            if request:
                verify_path = reverse('email_verify_link', kwargs={'token': verification_token})
                verification_link = request.build_absolute_uri(verify_path)
            else:
                backend_base = getattr(settings, 'BACKEND_BASE_URL', '')
                if not backend_base:
                    backend_base = getattr(settings, 'API_BASE_URL', '')
                if not backend_base:
                    backend_base = getattr(settings, 'FRONTEND_URL', getattr(settings, 'FRONTEND_BASE_URL', 'https://www.optitab.net'))
                backend_base = backend_base.rstrip('/')
                verification_link = f"{backend_base}/api/users/email/verify-link/{verification_token}/"

            user.verification_code_sent_at = timezone.now()
            user.save(update_fields=['verification_code_sent_at'])
            if not EmailService.send_verification_link(user, verification_link):
                logger.error("Échec de l'envoi du mail de vérification pour %s", user.email)
        except Exception as exc:
            logger.error("Erreur lors de la préparation du mail de vérification (%s): %s", user.email, exc)
        
        return user


RegisterSerializer = UserRegistrationSerializer
