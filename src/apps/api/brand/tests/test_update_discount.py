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


class BrandDiscountUpdateApiTestCase(AuthenticatedBrandAPITestCase):
    def test_should_update(self):
        brand = self.mixer.blend(models.Brand)
        self.authenticated(brand)

        discount = self.mixer.blend(models.Discount, brand=brand)

        response = self.client.put(reverse('api:brand-discount-update', args=[discount.pk]), data={
            "code": self.faker.name(),
            "description": self.faker.name(),
            "quantity": 100,
            "hide": True,
            "enable": False
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertSchema(DiscountSchema, data)

    def test_should_not_update_if_is_user(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        new_website = self.faker.url()
        new_name = self.faker.name()

        response = self.client.put(reverse('api:brand-discount-update', args=[uuid.uuid4()]), data={
            'website': new_website,
            'name': new_name,
        })

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_update_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        new_website = self.faker.url()
        new_name = self.faker.name()
        response = self.client.put(reverse('api:brand-discount-update', args=[uuid.uuid4()]), data={
            'website': new_website,
            'name': new_name,
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
