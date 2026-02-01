from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import os
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.renderers import TemplateHTMLRenderer
import logging
import re

logger = logging.getLogger(__name__)


class AdminRequiredMixin(APIView):
    """
    Mixin to ensure only admin users can access the view
    """
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().dispatch(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint pour Render
    """
    return Response({
        'status': 'healthy',
        'timestamp': request.GET.get('timestamp', 'N/A'),
        'environment': 'production' if not os.getenv('DEBUG', 'False').lower() == 'true' else 'development'
    }, status=status.HTTP_200_OK)

@require_GET
@cache_page(60 * 15)  # Cache 15 minutes
def status_view(request):
    """
    Status view for monitoring
    """
    return JsonResponse({
        'status': 'ok',
        'service': 'OptiTAB Backend',
        'version': '1.0.0'
    })


class RootView(APIView):
    """
    Root view for the API that provides basic information about available endpoints.
    """
    permission_classes = [AllowAny]
    # Serve a friendly HTML landing page for browsers,
    # and JSON for API clients via content negotiation.
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get(self, request):
        """
        Return API information and available endpoints.
        """
        data = {
            "message": "OptiTAB API Server",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "admin": "/admin/",
                "users": "/api/users/",
                "curriculum": "/api/",
                "courses": "/api/cours/",
                "synthesis": "/api/",
                "tracking": "/api/suivis/",
                "calculator": "/api/calc/",
                "quizzes": "/api/quiz/",
                "countries": "/api/",
                "ai": "/api/ai/"
            },
            "documentation": "API documentation available at /api/docs/"
        }
        # If browser requests HTML, render a simple landing page template.
        # Otherwise, fall back to JSON.
        return Response(data, template_name='core/index.html')


def root_json_view(request):
    """
    Root endpoint without DRF Browsable UI. Always returns pure JSON.
    """
    data = {
        "message": "OptiTAB API Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "admin": "/admin/",
            "users": "/api/users/",
            "curriculum": "/api/",
            "courses": "/api/cours/",
            "synthesis": "/api/",
            "tracking": "/api/suivis/",
            "calculator": "/api/calc/",
            "quizzes": "/api/quiz/",
            "countries": "/api/",
            "ai": "/api/ai/"
        },
        "documentation": "API documentation available at /api/docs/"
    }
    return JsonResponse(data)


def redirect_to_frontend(request, path=""):
    """
    Redirect any non-API/admin path received by the backend to the frontend
    static site, preserving the requested path.

    This is useful when the apex domain accidentally points to the backend
    service: hitting e.g. "/dashboard" on the backend will issue a 301 to
    the configured frontend base URL with the same path.

    Note: This function now explicitly checks that the path doesn't start
    with 'admin/' or 'api/' to avoid conflicts with Django admin and API routes.
    """
    # Don't redirect admin or API paths
    if path.startswith(('admin/', 'api/')):
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound("Page not found")

    base_url = getattr(settings, 'FRONTEND_BASE_URL', 'https://www.optitab.net')
    base_url = base_url.rstrip('/')
    preserved_path = ("/" + path.lstrip('/')) if path else "/"
    return HttpResponsePermanentRedirect(f"{base_url}{preserved_path}")


# ================================
# API: Contact form submission
# ================================

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def contact_send(request):
    """Réception du formulaire de contact et envoi d'email à l'équipe OptiTAB.

    Body JSON attendu:
    {
      "firstName": "",
      "lastName": "",
      "email": "",
      "subject": "",
      "message": ""
    }
    """
    from .services import EmailService, ResponseService

    data = request.data or {}
    first = (data.get("firstName") or "").strip()
    last = (data.get("lastName") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}
    if not first:
        errors["firstName"] = "Champ requis"
    if not last:
        errors["lastName"] = "Champ requis"
    if not email or not EMAIL_REGEX.match(email):
        errors["email"] = "Email invalide"
    if not subject:
        errors["subject"] = "Champ requis"
    if not message or len(message) < 5:
        errors["message"] = "Message trop court"

    if errors:
        return ResponseService.validation_error(errors)

    ok = EmailService.send_contact_message(first, last, email, subject, message)
    if not ok:
        return ResponseService.error(
            message="Impossible d'envoyer votre message pour le moment.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Envoi de l'email de confirmation à l'expéditeur (erreur non bloquante)
    try:
        EmailService.send_contact_confirmation(email, first, subject, message)
    except Exception:  # déjà loggé dans le service
        pass

    return ResponseService.success(
        message="Message envoyé avec succès. Nous vous répondrons sous 24h.",
        status_code=status.HTTP_200_OK,
    )
