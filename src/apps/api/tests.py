from apps.api.permissions import UserRoleEnum
from apps.domain import models
from commons.tests.base import APITestCase


class AuthenticatedAPITestCase(APITestCase):
    auth_user_model = None
    user = None

    def setUp(self) -> None:
        if self.auth_user_model:
            # create a default panel_user for tests.
            self.user = self.mixer.blend(self.auth_user_model)

            # define default authenticated panel_user.
            self.authenticated(self.user)

    def authenticated(self, user):
        """
        Set authentication header to request client.
        """
        if isinstance(user, models.User):
            role = UserRoleEnum.USER.value

        elif isinstance(user, models.Brand):
            role = UserRoleEnum.BRAND.value

        else:
            raise TypeError("Instance must be 'domain.models.User' type.")

        self.client.defaults["HTTP_AUTHORIZATION"] = f"{role} {user.pk}"

    def unauthenticated(self):
        """
        Clear authentication header from request client.
        """
        if "HTTP_AUTHORIZATION" in self.client.defaults:
            del self.client.defaults["HTTP_AUTHORIZATION"]


class AuthenticatedUserAPITestCase(AuthenticatedAPITestCase):
    """
    Use when the default authenticated panel_user is a User.
    """

    auth_user_model = models.User


class AuthenticatedBrandAPITestCase(AuthenticatedAPITestCase):
    """
    Use when the default authenticated panel_user is a Brand.
    """

    auth_user_model = models.User
