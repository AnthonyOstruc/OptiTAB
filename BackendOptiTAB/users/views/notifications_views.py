from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserNotification
from users.serializers.user_profile import UserNotificationSerializer


class UserNotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer

    def get_queryset(self):
        qs = UserNotification.objects.filter(user=self.request.user)
        only_unread = self.request.query_params.get('unread')
        if only_unread in ['1', 'true', 'True']:
            qs = qs.filter(read=False)
        return qs.order_by('-created_at', '-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        # Autoriser PATCH pour marquer comme lu
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


