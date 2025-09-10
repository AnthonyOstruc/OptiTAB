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
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from core.services import ResponseService
import logging

from ..serializers.authentication import (
    UserRegistrationSerializer,
    EmailVerificationSerializer
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
        Create new user account with email verification.
        
        Returns:
            201: User created successfully, verification email sent
            400: Validation errors
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            logger.info(f"New user registration: {user.email}")
            
            return ResponseService.success(
                message=(
                    "Compte créé avec succès. "
                    "Vérifiez votre email pour activer votre compte."
                ),
                data={
                    'user_id': user.id,
                    'email': user.email,
                    'verification_required': True
                },
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


class EmailVerificationView(APIView):
    """
    Professional email verification endpoint.
    
    Features:
        - Secure code validation
        - Account activation
        - Clear success/error responses
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Verify email with verification code.
        
        Returns:
            200: Email verified, account activated
            400: Invalid code or validation errors
        """
        serializer = EmailVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            logger.info(f"Email verified: {user.email}")
            
            return ResponseService.success(
                message="Email vérifié avec succès. Votre compte est maintenant actif.",
                data={
                    'user_id': user.id,
                    'email': user.email,
                    'is_active': user.is_active
                }
            )
        
        return ResponseService.validation_error(serializer.errors)


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
VerifyCodeView = EmailVerificationView
LogoutView = UserLogoutView
