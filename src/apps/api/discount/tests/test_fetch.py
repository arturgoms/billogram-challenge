import uuid

from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedBrandAPITestCase
from apps.domain import models
from commons import json_schema


class DiscountsSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    code = json_schema.StringProperty()
    description = json_schema.StringProperty()


class UserDiscountFetchApiTestCase(AuthenticatedBrandAPITestCase):
    def test_should_list(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        discount = self.mixer.blend(models.Discount)

        response = self.client.get(reverse('api:discount-fetch', args=[discount.pk]))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        data = response.json()

        self.assertSchema(DiscountsSchema, data)

    def test_should_not_fetch_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse('api:discount-fetch', args=[uuid.uuid4()]))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_should_not_fetch_if_already_taken(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        discount = self.mixer.blend(models.Discount)

        response = self.client.get(reverse('api:discount-fetch', args=[discount.pk]))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response = self.client.get(reverse('api:discount-fetch', args=[discount.pk]))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_should_not_fetch_if_balance_is_zero(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        user2 = self.mixer.blend(models.User)
        discount = self.mixer.blend(models.Discount, quantity=1)
        self.mixer.blend(models.UserDiscount, user=user2, discount=discount)

        response = self.client.get(reverse('api:discount-fetch', args=[discount.pk]))
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, response.status_code)

    def test_should_not_fetch_if_discount_is_disabled(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        discount = self.mixer.blend(models.Discount, enable=False)

        response = self.client.get(reverse('api:discount-fetch', args=[discount.pk]))
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, response.status_code)

