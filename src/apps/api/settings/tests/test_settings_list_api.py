from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedUserAPITestCase
from commons import json_schema


class SettingsSchema(json_schema.JsonSchema):
    key = json_schema.StringProperty()
    value = json_schema.MixedTypeProperty(
        types=[json_schema.StringProperty, json_schema.NumberProperty], nullable=True
    )


class SettingsListApiTestCase(AuthenticatedUserAPITestCase):
    def test_should_list(self):
        response = self.client.get(reverse("api:settings-list"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertListSchema(SettingsSchema, data)

    def test_should_not_list_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(reverse("api:settings-list"))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
