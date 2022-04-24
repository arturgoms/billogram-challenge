from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedBrandAPITestCase
from apps.domain import models
from commons import json_schema


class BrandSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    name = json_schema.StringProperty()
    website = json_schema.StringProperty()


class DiscountSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    description = json_schema.StringProperty()
    code = json_schema.StringProperty()
    brand = json_schema.ObjectProperty(schema=BrandSchema)


class DiscountsSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    discount = json_schema.ObjectProperty(schema=DiscountSchema)


class UserDiscountListApiTestCase(AuthenticatedBrandAPITestCase):
    def test_should_list(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        self.mixer.cycle(10).blend(models.UserDiscount, user=user)

        response = self.client.get(reverse('api:user-discount-list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertPaginatedSchema(DiscountsSchema, data)

    def test_should_not_list_for_brand(self):
        brand = self.mixer.blend(models.Brand)

        # Set user token.
        self.authenticated(brand)

        response = self.client.get(reverse('api:user-discount-list'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_list_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse('api:user-discount-list'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
