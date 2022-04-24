import uuid

from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedBrandAPITestCase
from apps.domain import models
from commons import json_schema


class DiscountSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    code = json_schema.StringProperty()
    description = json_schema.StringProperty()
    quantity = json_schema.IntegerProperty()
    hide = json_schema.BooleanProperty()
    enable = json_schema.BooleanProperty()


class BrandDiscountCreateApiTestCase(AuthenticatedBrandAPITestCase):
    def test_should_create(self):
        brand = self.mixer.blend(models.Brand)
        self.authenticated(brand)

        response = self.client.post(
            reverse("api:brand-discount-create"),
            data={
                "code": self.faker.name(),
                "description": self.faker.name(),
                "quantity": 100,
                "hide": True,
                "enable": False,
            },
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        data = response.json()

        self.assertSchema(DiscountSchema, data)

    def test_should_not_create_for_user(self):
        user = self.mixer.blend(models.User)

        # Set user token.
        self.authenticated(user)

        response = self.client.post(reverse("api:brand-discount-create"))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_create_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse("api:brand-discount-create"))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
