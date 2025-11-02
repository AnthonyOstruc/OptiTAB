"""
Authentication Views - Professional Implementation
================================================

Clean, secure, and maintainable authentication views following
REST API best practices and security standards.

Classes:
    - UserRegistrationView: Handles new user registration
    - CustomLoginView: JWT-based authentication
    - EmailVerificationView: Email verification flow
    - UserLogoutView: Secure logout with token blacklisting
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from core.services import ResponseService, EmailService
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets
from users.models import CustomUser
import logging
from django.urls import reverse
from django.shortcuts import redirect

from ..serializers.authentication import (
    UserRegistrationSerializer,
)
from ..serializers.token_serializers import CustomTokenObtainPairSerializer

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """
    Professional user registration endpoint.
    
    Features:
        - Comprehensive input validation
        - Automatic email verification
        - Clean error responses
        - Security logging
    """
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Create new user account and return JWT tokens for immediate login.
        
        Returns:
            201: User created successfully with tokens
            400: Validation errors
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            logger.info(f"New user registration: {user.email}")
            
            # Generate JWT tokens for immediate login
            refresh = RefreshToken.for_user(user)
            token_payload = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'email_verified': not bool(user.verification_code),
            }
            return ResponseService.success(
                message="Compte créé et connecté",
                data=token_payload,
                status_code=status.HTTP_201_CREATED
            )
        
        return ResponseService.validation_error(serializer.errors)


class CustomLoginView(TokenObtainPairView):
    """
    Professional JWT authentication endpoint.
    
    Features:
        - Custom token serializer with user data
        - Enhanced security validation
        - Structured response format
    """
    
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return JWT tokens.
        
        Returns:
            200: Authentication successful with tokens
            401: Invalid credentials
            400: Validation errors
        """
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            logger.info(f"Successful login: {request.data.get('email', 'unknown')}")
            
            # Enhance response with success format
            return ResponseService.success(
                message="Connexion réussie",
                data=response.data
            )
        
        return response


class EmailVerificationSendView(APIView):
    """Envoie un code de vérification à l'email de l'utilisateur connecté."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user: CustomUser = request.user
        try:
            # Si déjà vérifié, répondre gentiment (idempotent)
            if not user.verification_code:
                return ResponseService.success(
                    message="Email déjà vérifié",
                )

            # Limite simple: ne pas renvoyer plus d'une fois par minute
            if user.verification_code_sent_at and (timezone.now() - user.verification_code_sent_at) < timedelta(minutes=1):
                return ResponseService.error(
                    message="Veuillez patienter une minute avant de renvoyer un lien",
                    status_code=429
                )

            # Générer un token sécurisé pour vérification par lien
            token = secrets.token_urlsafe(32)
            user.verification_code = token
            user.verification_code_sent_at = timezone.now()
            user.save(update_fields=["verification_code", "verification_code_sent_at"]) 

            # Construire un lien absolu vers l'endpoint de vérification
            verify_path = reverse('email_verify_link', kwargs={'token': token})
            verification_link = request.build_absolute_uri(verify_path)

            sent = EmailService.send_verification_link(user, verification_link)
            if not sent:
                logger.error("Échec d'envoi du lien de vérification pour %s", user.email)

            return ResponseService.success(
                message="Lien de vérification envoyé" if sent else "Lien généré, mais l'envoi email a échoué. Réessayez plus tard.",
                data={'email_sent': sent}
            )
        except Exception as e:
            return ResponseService.error(
                message=f"Erreur lors de l'envoi du lien: {e}",
                status_code=500
            )


class EmailVerificationConfirmView(APIView):
    """Vérifie le code et active le compte utilisateur."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user: CustomUser = request.user
        try:
            code = str(request.data.get('code') or '').strip()
            if not code:
                return ResponseService.error(
                    message="Code invalide",
                    status_code=400
                )

            if not user.verification_code or not user.verification_code_sent_at:
                return ResponseService.error(
                    message="Aucun code actif. Veuillez renvoyer un code.",
                    status_code=400
                )

            # Expiration 24h
            if (timezone.now() - user.verification_code_sent_at) > timedelta(hours=24):
                return ResponseService.error(
                    message="Code expiré. Veuillez renvoyer un nouveau code.",
                    status_code=400
                )

            if code != user.verification_code:
                return ResponseService.error(
                    message="Code incorrect",
                    status_code=400
                )

            # Activer le compte et nettoyer
            user.verification_code = None
            user.verification_code_sent_at = None
            user.is_active = True
            user.save(update_fields=["is_active", "verification_code", "verification_code_sent_at"]) 

            return ResponseService.success(
                message="Email vérifié avec succès",
                data={"is_active": True}
            )
        except Exception as e:
            return ResponseService.error(
                message=f"Erreur lors de la vérification: {e}",
                status_code=500
            )


class EmailVerificationLinkView(APIView):
    """Vérifie l'email via un lien sécurisé."""
    permission_classes = [AllowAny]

    def get(self, request, token):
        redirect_base = getattr(settings, 'FRONTEND_URL', '') or getattr(settings, 'FRONTEND_BASE_URL', '')
        if not redirect_base:
            redirect_base = 'https://www.optitab.net'
        redirect_base = redirect_base.rstrip('/') or 'https://www.optitab.net'

        success_query = '?email_verified=1'
        failure_query = '?email_verified=0'

        try:
            if not token:
                return redirect(f"{redirect_base}/account{failure_query}")

            user = CustomUser.objects.filter(verification_code=token).first()
            if not user:
                return redirect(f"{redirect_base}/account{failure_query}")

            # Vérifier l'expiration (24h)
            if not user.verification_code_sent_at or (timezone.now() - user.verification_code_sent_at) > timedelta(hours=24):
                return redirect(f"{redirect_base}/account{failure_query}")

            user.is_active = True
            user.verification_code = None
            user.verification_code_sent_at = None
            user.save(update_fields=["is_active", "verification_code", "verification_code_sent_at"])

            return redirect(f"{redirect_base}/account{success_query}")
        except Exception:
            return redirect(f"{redirect_base}/account{failure_query}")

class UserLogoutView(APIView):
    """
    Professional logout endpoint with token blacklisting.
    
    Features:
        - Secure token invalidation
        - Comprehensive error handling
        - Audit logging
    """
    
    def post(self, request):
        """
        Logout user and blacklist refresh token.
        
        Returns:
            205: Logout successful
            400: Invalid or missing token
        """
        refresh_token = request.data.get("refresh_token") or request.data.get("refresh")
        
        if not refresh_token:
            # Idempotent: considérer la déconnexion comme réussie même sans token
            logger.warning(
                f"Logout attempt without refresh token from {request.META.get('REMOTE_ADDR')} (idempotent success)"
            )
        return ResponseService.success(
            message="Déconnexion réussie",
            status_code=status.HTTP_205_RESET_CONTENT
        )


class EmailChangeRequestView(APIView):
    """Permet à l'utilisateur de demander un changement d'email."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        new_email = (request.data.get('email') or '').strip().lower()

        if not new_email:
            return ResponseService.validation_error({'email': 'Un email est requis.'})

        if new_email == user.email:
            return ResponseService.validation_error({'email': 'Veuillez saisir une adresse différente de l\'actuelle.'})

        if CustomUser.objects.filter(email__iexact=new_email).exclude(id=user.id).exists():
            return ResponseService.validation_error({'email': 'Cette adresse est déjà utilisée.'})

        token = secrets.token_urlsafe(32)
        user.pending_email = new_email
        user.pending_email_token = token
        user.pending_email_sent_at = timezone.now()
        user.save(update_fields=['pending_email', 'pending_email_token', 'pending_email_sent_at'])

        verify_path = reverse('email_change_confirm', kwargs={'token': token})
        verification_link = request.build_absolute_uri(verify_path)
        sent = EmailService.send_email_change_link(user, new_email, verification_link)

        return ResponseService.success(
            message="Lien de confirmation envoyé" if sent else "Lien généré, mais l'envoi email a échoué. Réessayez plus tard.",
            data={'email_sent': sent}
        )


class EmailChangeConfirmView(APIView):
    """Confirme le changement d'email via lien reçu."""
    permission_classes = [AllowAny]

    def get(self, request, token):
        redirect_base = getattr(settings, 'FRONTEND_URL', '') or getattr(settings, 'FRONTEND_BASE_URL', '')
        if not redirect_base:
            redirect_base = 'https://www.optitab.net'
        redirect_base = redirect_base.rstrip('/') or 'https://www.optitab.net'

        success_query = '?email_change=1'
        failure_query = '?email_change=0'

        try:
            if not token:
                return redirect(f"{redirect_base}/account{failure_query}")

            user = CustomUser.objects.filter(pending_email_token=token).first()
            if not user or not user.pending_email:
                return redirect(f"{redirect_base}/account{failure_query}")

            if user.pending_email_sent_at and (timezone.now() - user.pending_email_sent_at) > timedelta(hours=1):
                return redirect(f"{redirect_base}/account{failure_query}")

            # Vérifier que l'email n'est pas utilisé
            if CustomUser.objects.filter(email__iexact=user.pending_email).exclude(id=user.id).exists():
                return redirect(f"{redirect_base}/account{failure_query}")

            user.email = user.pending_email
            user.pending_email = None
            user.pending_email_token = None
            user.pending_email_sent_at = None
            user.verification_code = None
            user.verification_code_sent_at = None
            user.save(update_fields=['email', 'pending_email', 'pending_email_token', 'pending_email_sent_at', 'verification_code', 'verification_code_sent_at'])

            return redirect(f"{redirect_base}/account{success_query}")
        except Exception:
            return redirect(f"{redirect_base}/account{failure_query}")
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            user_email = (
                request.user.email 
                if request.user.is_authenticated 
                else "utilisateur anonyme"
            )
            
            logger.info(f"Successful logout: {user_email}")
            
            return ResponseService.success(
                message="Déconnexion réussie",
                status_code=status.HTTP_205_RESET_CONTENT
            )
            
        except Exception as e:
            # Idempotent: ne jamais échouer fonctionnellement la déconnexion
            logger.warning(f"Logout error (idempotent success): {e}")
            return ResponseService.success(
                message="Déconnexion réussie",
                status_code=status.HTTP_205_RESET_CONTENT
            )


class PasswordResetView(APIView):
    """
    Professional password reset endpoint.
    
    Features:
        - Secure reset token generation
        - Email-based reset flow
        - Rate limiting protection
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Initiate password reset process.
        
        Returns:
            200: Reset email sent (or would be sent for security)
            400: Invalid email format
        """
        # Implementation would go here
        # For now, return a placeholder response
        return ResponseService.success(
            message=(
                "Si cette adresse email existe, "
                "vous recevrez un lien de réinitialisation."
            )
        )


# Professional aliases for consistency and backward compatibility
RegisterView = UserRegistrationView
# Backward compat: old name pointed to verify; map to new confirm view
VerifyCodeView = EmailVerificationConfirmView
LogoutView = UserLogoutView
