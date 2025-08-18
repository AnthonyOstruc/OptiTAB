"""
Core views providing base functionality and common patterns.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class BasePermissionMixin:
    """
    Mixin providing common permission logic.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]


class BaseFilterMixin:
    """
    Mixin providing common filtering functionality.
    """
    
    def filter_by_user(self, queryset):
        """
        Filter queryset by current user if applicable.
        """
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            if hasattr(queryset.model, 'user'):
                return queryset.filter(user=self.request.user)
        return queryset

    def filter_by_active(self, queryset):
        """
        Filter queryset to show only active items.
        """
        if hasattr(queryset.model, 'est_actif'):
            return queryset.filter(est_actif=True)
        return queryset

    def apply_common_filters(self, queryset):
        """
        Apply common filters to queryset.
        """
        # Filter by active status unless explicitly requesting inactive items
        if not self.request.query_params.get('include_inactive', False):
            queryset = self.filter_by_active(queryset)
        
        return queryset


class BaseViewSet(BasePermissionMixin, BaseFilterMixin, viewsets.ModelViewSet):
    """
    Base ViewSet with common functionality for all model viewsets.
    """
    
    def get_queryset(self):
        """
        Get the queryset with common filters applied.
        """
        queryset = super().get_queryset()
        return self.apply_common_filters(queryset)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer based on action.
        """
        if hasattr(self, 'serializer_classes'):
            return self.serializer_classes.get(self.action, self.serializer_class)
        
        # Default behavior: use different serializers for different actions
        if self.action in ['create', 'update', 'partial_update']:
            if hasattr(self, 'write_serializer_class'):
                return self.write_serializer_class
        elif self.action == 'list':
            if hasattr(self, 'list_serializer_class'):
                return self.list_serializer_class
        
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Hook to modify object creation.
        """
        # Automatically assign user if model has user field
        if hasattr(serializer.Meta.model, 'user') and hasattr(self.request, 'user'):
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def handle_exception(self, exc):
        """
        Handle exceptions with consistent error formatting.
        """
        logger.error(f"Exception in {self.__class__.__name__}: {str(exc)}")
        
        if isinstance(exc, ValidationError):
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().handle_exception(exc)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Common endpoint to get statistics about the model.
        """
        queryset = self.get_queryset()
        total_count = queryset.count()
        
        stats_data = {
            'total': total_count,
        }
        
        # Add active/inactive counts if model supports it
        if hasattr(queryset.model, 'est_actif'):
            stats_data.update({
                'active': queryset.filter(est_actif=True).count(),
                'inactive': queryset.filter(est_actif=False).count(),
            })
        
        return Response(stats_data)


class BaseAPIView(BasePermissionMixin, APIView):
    """
    Base API view with common functionality.
    """
    
    def handle_exception(self, exc):
        """
        Handle exceptions with consistent error formatting.
        """
        logger.error(f"Exception in {self.__class__.__name__}: {str(exc)}")
        
        if isinstance(exc, ValidationError):
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().handle_exception(exc)


class ReadOnlyViewSet(BaseFilterMixin, viewsets.ReadOnlyModelViewSet):
    """
    Base read-only ViewSet for models that should not be modified via API.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get the queryset with common filters applied.
        """
        queryset = super().get_queryset()
        return self.apply_common_filters(queryset)


class AdminRequiredMixin:
    """
    Mixin that requires admin permissions for all actions.
    """
    permission_classes = [permissions.IsAdminUser]


class UserScopedMixin(BaseFilterMixin):
    """
    Mixin that automatically scopes queries to the current user.
    """
    
    def get_queryset(self):
        """
        Filter queryset to current user's data only.
        """
        queryset = super().get_queryset()
        return self.filter_by_user(queryset)
