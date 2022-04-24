from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedUserAPITestCase
from apps.domain import models
from commons import json_schema


class ProfileSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    first_name = json_schema.StringProperty()
    last_name = json_schema.StringProperty()
    email = json_schema.EmailProperty()


class UserProfileApiTestCase(AuthenticatedUserAPITestCase):
    def test_should_retrieve(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)
        response = self.client.get(reverse("api:user-profile"))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertSchema(ProfileSchema, response.json())

    def test_should_update(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        new_name = self.faker.name()
        new_name_last = self.faker.name()
        response = self.client.put(
            reverse("api:user-profile"),
            data={
                "first_name": new_name,
                "last_name": new_name_last,
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertEqual(data["first_name"], new_name)
        self.assertEqual(data["last_name"], new_name_last)
        self.assertSchema(ProfileSchema, data)

    def test_should_not_update_if_is_brand(self):
        brand = self.mixer.blend(models.Brand)
        self.authenticated(brand)

        new_name = self.faker.name()
        new_name_last = self.faker.name()
        response = self.client.put(
            reverse("api:user-profile"),
            data={
                "first_name": new_name,
                "last_name": new_name_last,
            },
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_update_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        new_name = self.faker.name()
        new_name_last = self.faker.name()
        response = self.client.put(
            reverse("api:user-profile"),
            data={
                "first_name": new_name,
                "last_name": new_name_last,
            },
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_should_not_retrieve_for_brand(self):
        brand = self.mixer.blend(models.Brand)

        # set authentication header
        self.authenticated(brand)

        response = self.client.get(reverse("api:user-profile"))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_retrieve_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse("api:user-profile"))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
