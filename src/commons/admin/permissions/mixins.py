from commons.admin.permissions.helper import PermissionHelper


class PermissionsAdminMixin:
    """
    Add support to permissions.
    """

    permission_helper = PermissionHelper()
    module_permission = ["view", "add", "change", "delete"]

    def has_add_permission(self, request):
        return self.permission_helper.has_permission(
            user=request.user, context=self.__class__.__name__, action="add"
        )

    def has_change_permission(self, request, obj=None):
        return self.permission_helper.has_permission(
            user=request.user, context=self.__class__.__name__, action="change"
        )

    def has_delete_permission(self, request, obj=None):
        return self.permission_helper.has_permission(
            user=request.user, context=self.__class__.__name__, action="delete"
        )

    def has_view_permission(self, request, obj=None):
        return self.permission_helper.has_permission(
            user=request.user, context=self.__class__.__name__, action="view"
        )

    def has_module_permission(self, request):
        return any(
            self.permission_helper.has_permission(
                user=request.user, context=self.__class__.__name__, action=module
            )
            for module in self.module_permission
        )
