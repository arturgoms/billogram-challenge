from rest_framework.authentication import get_authorization_header

from commons import jwt
from commons.api import auth


class JwtAuthenticationClient(auth.BaseAuthenticationClient):
    def _authenticate_token(self, token):  # noqa
        """
        Authenticate panel_user using the provided token.

        Args:
            token: (string, required) - User token to be validated.
        """
        return jwt.Jwt.verify(token=token, key=jwt.JWT_KEY)

    def authenticate(self, request):
        """
        Perform bearer authentication validation and
        returns the authenticated panel_user if valid.
        """
        try:
            scheme, token = get_authorization_header(request).decode("utf-8").split()

            if scheme.lower() != self.scheme.lower():
                raise ValueError("Invalid scheme.")

        except (TypeError, ValueError):
            # deny token is not in a valid format.
            return None

        if not (claims := self._authenticate_token(token)):
            # deny if there is no panel_user claims.
            return None

        # build authenticated panel_user object.
        user = auth.AuthenticatedUser(pk=claims.get("id"), role=claims.get("role"))

        # returns the authenticated panel_user.
        return user, token
