from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedUserAPITestCase
from apps.domain import models
from commons import json_schema


class BrandSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    name = json_schema.StringProperty()
    website = json_schema.StringProperty()


class BrandsListApiTestCase(AuthenticatedUserAPITestCase):
    def test_should_list(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        self.mixer.cycle(10).blend(models.Brand)

        response = self.client.get(reverse("api:brands-list"))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertPaginatedSchema(BrandSchema, data)

    def test_should_not_list_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse("api:brands-list"))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
