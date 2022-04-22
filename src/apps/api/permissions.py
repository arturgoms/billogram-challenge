from enum import Enum

from rest_framework.permissions import BasePermission


class UserRoleEnum(Enum):
    USER = 1

    @classmethod
    def is_user(cls, user):
        return user.role == cls.USER.value


class BaseRolePermission(BasePermission):
    http_allowed_verbs = ["HEAD", "OPTIONS"]

    def is_allowed_verb(self, request):
        """
        Check whether the http verb is allowed.
        """
        return request.method in self.http_allowed_verbs

    def is_authenticated(self, request):  # noqa
        """
        Check whether the user is authenticated.
        """
        return request.user and request.user.is_authenticated

    def has_role_permission(self, request):
        """
        Check whether user has the role permission.
        """
        raise NotImplementedError()

    def has_permission(self, request, view):
        """
        Check whether the user is allowed to perform
        actions in the given request.
        """
        if self.is_allowed_verb(request):
            return True

        return self.is_authenticated(request) and self.has_role_permission(request)


class IsClient(BaseRolePermission):
    """
    The request is authenticated as a client user, or cors http verbs.
    """

    def has_role_permission(self, request):
        return UserRoleEnum.is_user(request.user)
