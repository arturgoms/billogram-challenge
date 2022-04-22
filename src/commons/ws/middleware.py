from commons import jwt
from commons.api import auth


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes panel_user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser

        # Look up panel_user from query string (you should also do things like
        # checking if it is a valid panel_user ID, or if scope["panel_user"] is already
        # populated).
        headers = {key.decode(): val.decode() for key, val in scope["headers"]}

        token = headers["authorization"].split()[1]

        try:
            if not (claims := jwt.Jwt.verify(token=token, key=jwt.JWT_KEY)):
                # deny if there is no panel_user claims.
                return None

            scope["panel_user"] = auth.AuthenticatedUser(
                pk=claims.get("id"), role=claims.get("role")
            )

        except (TypeError, ValueError):
            scope["panel_user"] = AnonymousUser()

        return await self.app(scope, receive, send)
