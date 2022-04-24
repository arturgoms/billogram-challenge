from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedBrandAPITestCase
from apps.domain import models
from commons import json_schema


class ProfileSchema(json_schema.JsonSchema):
    id = json_schema.UUIDProperty()
    website = json_schema.StringProperty()
    name = json_schema.StringProperty()
    email = json_schema.EmailProperty()


class BrandProfileApiTestCase(AuthenticatedBrandAPITestCase):

    def test_should_retrieve(self):
        brand = self.mixer.blend(models.Brand)
        self.authenticated(brand)
        response = self.client.get(reverse('api:brand-profile'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertSchema(ProfileSchema, response.json())

    def test_should_update(self):
        brand = self.mixer.blend(models.Brand)
        self.authenticated(brand)

        new_website = self.faker.url()
        new_name = self.faker.name()
        response = self.client.put(reverse('api:brand-profile'), data={
            'website': new_website,
            'name': new_name,
        })

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertEqual(data['name'], new_name)
        self.assertEqual(data['website'], new_website)
        self.assertSchema(ProfileSchema, data)

    def test_should_not_update_if_is_user(self):
        user = self.mixer.blend(models.User)
        self.authenticated(user)

        new_website = self.faker.url()
        new_name = self.faker.name()
        response = self.client.put(reverse('api:brand-profile'), data={
            'website': new_website,
            'name': new_name,
        })

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_update_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        new_website = self.faker.url()
        new_name = self.faker.name()
        response = self.client.put(reverse('api:brand-profile'), data={
            'website': new_website,
            'name': new_name,
        })

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_should_not_retrieve_for_user(self):
        user = self.mixer.blend(models.User)

        # set authentication header
        self.authenticated(user)

        response = self.client.get(reverse('api:brand-profile'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_should_not_retrieve_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse('api:brand-profile'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)