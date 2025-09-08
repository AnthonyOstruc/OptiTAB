from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import os

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