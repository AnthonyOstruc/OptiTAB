from rest_framework.permissions import BasePermission


class IsStaffOrSuperuser(BasePermission):
    """Allow access only to authenticated staff or superusers."""

    message = 'Acces reserve aux administrateurs et staff.'

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return bool(getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False))
