import uuid

from django.conf import settings
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from rest_framework import authentication

AUTHENTICATION_CLIENT = getattr(settings, "AUTHENTICATION_CLIENT")


def get_authentication_client():
    """
    Returns the defined authentication client for the project.
    """
    return import_string(AUTHENTICATION_CLIENT)()


class BaseAuthenticationClient:
    """
    Provides the ability to authenticate by using request.
    """

    scheme = "bearer"

    def authenticate(self, request):
        """
        Perform user authentication based on request.
        """
        raise NotImplementedError()


class ClientAuthentication(authentication.BaseAuthentication):
    @cached_property
    def client(self):
        """
        Returns a instance of the authentication client.
        """
        return get_authentication_client()

    def authenticate(self, request):
        """
        Uses firebase client to authenticate a
        user based on a request token.
        """
        return self.client.authenticate(request)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return "WWW-Authenticate"


class AuthenticatedUser:
    """
    Object to represent an authenticated user.
    """

    _db_representation_error = (
        "Django does not provide a DB representation for '{name}'."
    )

    USERNAME_FIELD = "pk"

    is_superuser = False
    is_staff = False
    is_anonymous = False
    is_authenticated = True
    is_active = True

    def __init__(self, pk, role, **kwargs):
        self.pk = self.id = uuid.UUID(pk)

        try:
            self.role = int(role)

        except (TypeError, ValueError):
            self.role = None

        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.pk}>"

    def get_username(self):
        return getattr(self, AuthenticatedUser.USERNAME_FIELD, None)

    def save(self):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )

    def delete(self):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )

    def set_password(self, raw_password):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )

    def check_password(self, raw_password):
        raise NotImplementedError(
            self._db_representation_error.format(name=type(self).__name__)
        )
