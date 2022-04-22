from rest_framework.authentication import get_authorization_header

from commons.api import auth


class TestAuthenticationClient(auth.BaseAuthenticationClient):
    """
    Simple authentication that overrides the real
    authentication for tests.

    Header Example:

    ``Authorization: Email {email}``
    """

    def authenticate(self, request):
        try:
            role, identity = get_authorization_header(request).decode("utf-8").split()

        except (TypeError, ValueError):
            # deny token is not in a valid format.
            return None

        user = auth.AuthenticatedUser(pk=identity, role=role)

        return user, identity
