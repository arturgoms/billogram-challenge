from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        """
        Grant permission either the user is authenticated
        or it is a OPTIONS or HEAD http verb.

        Returns:
            bool
        """
        if request.method in {"HEAD", "OPTIONS"}:
            return True

        if request.user and request.user.is_authenticated:
            return True

        return False
