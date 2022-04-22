from django.conf import settings

from apps.domain.models import User


class PermissionHelper:
    def __init__(self):
        self.permissions = getattr(settings, "ADMIN_PERMISSIONS", {})

    def has_permission(self, user: User, context: str, action: str) -> bool:
        """
        Check if user has permission of that action
        """
        if user.is_superuser:
            return True

        if not user.is_authenticated:
            return False

        for role in user.roles:
            actions = ((self.permissions.get(role) or {}).get("permissions") or {}).get(
                context
            ) or []

            if action in actions:
                return True

        return False

    def has_permissions(self, user: User, context: str, actions: list) -> bool:
        """
        Check if user has the permissions in list
        """
        if user.is_superuser:
            return True

        if any(self.has_permission(user, context, action) for action in actions):
            return True

        return False

    def get_all_permissions(self) -> tuple:
        return tuple(map(lambda x: (x, self.permissions[x]["name"]), self.permissions))


# unique instance to be used.
permission_helper = PermissionHelper()
