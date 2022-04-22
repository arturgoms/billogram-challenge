from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    The request is authenticated as a user, or cors http verbs.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in ["HEAD", "OPTIONS"]
            or request.user
            and request.user.is_authenticated
        )


class IsPublic(BasePermission):
    """
    For public api endpoints, it is necessary to have at least a
    simple way to grant that only authorized consumers have access.

    This permission checks whether the consumer knows the access key
    to access these content.
    """

    message = _("Invalid authorization header.")

    scheme = getattr(settings, "PUBLIC_API_AUTHORIZATION_SCHEME", "public")
    access_key = getattr(settings, "PUBLIC_API_ACCESS_KEY", "")

    def is_authorized(self, request):
        """
        Verifies whether the authorization header is authorized.

        Args:
            request (Request, required): Current request instance.

        Returns:
            (bool, str)
        """
        try:
            scheme, access_key = (
                get_authorization_header(request).decode("utf-8").split()
            )

            if scheme.lower() != self.scheme.lower():
                raise ValueError("Invalid scheme.")

        except (TypeError, ValueError):
            # deny token is not in a valid format.
            return False

        else:
            return access_key == self.access_key

    def has_permission(self, request, view):
        """
        Ensure that only allowed consumers will have access to the content.
        """
        if request.method.lower() == "options":
            # if the request method is options just
            # allow the request.
            return True

        if request.user.is_authenticated:
            # All users can access the api using their own
            # authentication token. This will grant that authenticated
            # also have access to public apis.
            return True

        return self.is_authorized(request)
