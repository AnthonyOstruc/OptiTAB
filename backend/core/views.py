from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
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
import logging

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
    renderer_classes = [JSONRenderer]

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
        return Response(data)


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
