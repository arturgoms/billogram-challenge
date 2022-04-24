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


class BrandDiscountHistoryApiTestCase(AuthenticatedBrandAPITestCase):
    def test_should_retrieve(self):
        brand = self.mixer.blend(models.Brand)
        self.authenticated(brand)

        discount = self.mixer.blend(models.Discount, brand=brand)

        response = self.client.get(reverse('api:brand-discount-history', args=[discount.pk]))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertPaginatedSchema(DiscountSchema, data)

    def test_should_not_list_for_user(self):
        user = self.mixer.blend(models.User)

        # Set user token.
        self.authenticated(user)

        response = self.client.get(reverse('api:brand-discount-history', args=[uuid.uuid4()]))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_list_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse('api:brand-discount-history', args=[uuid.uuid4()]))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
