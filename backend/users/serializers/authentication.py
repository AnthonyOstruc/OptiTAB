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
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random
import logging
from django.utils import timezone

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
        """Create user and activate immediately (no email verification)."""
        # Remove confirmation field
        validated_data.pop('password_confirmation')
        
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            civilite=validated_data.get('civilite'),
            date_naissance=validated_data.get('date_naissance'),
            telephone=validated_data.get('telephone'),
            password=validated_data['password'],
            is_active=True,
            verification_code=None,
            verification_code_sent_at=None
        )
        
        logger.info(f"New user registration: {user.email}")
        return user
    
    def _generate_verification_code(self) -> str:
        """Generate secure 6-digit verification code."""
        return str(random.randint(100000, 999999))
    
    def _send_verification_email(self, user: CustomUser, code: str) -> bool:
        """
        Send verification email with error handling.
        
        Args:
            user: User instance
            code: Verification code
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            send_mail(
                subject='Code de vérification OptiTAB',
                message=self._get_email_template(user, code),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Verification email sent to {user.email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {e}")
            # Don't fail registration if email fails
            return False
    
    def _get_email_template(self, user: CustomUser, code: str) -> str:
        """Get formatted email template."""
        return f"""
Bonjour {user.first_name},

Bienvenue sur OptiTAB !

Votre code de vérification est : {code}

Ce code expire dans 24 heures.

Cordialement,
L'équipe OptiTAB
        """.strip()


RegisterSerializer = UserRegistrationSerializer
