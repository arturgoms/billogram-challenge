from django.urls import reverse
from rest_framework import status

from apps.api.tests import AuthenticatedUserAPITestCase
from commons import json_schema


class SettingsSchema(json_schema.JsonSchema):
    key = json_schema.StringProperty()
    value = json_schema.MixedTypeProperty(
        types=[json_schema.StringProperty, json_schema.NumberProperty], nullable=True
    )


class SettingsDetailApiTestCase(AuthenticatedUserAPITestCase):
    def test_should_retrieve(self):
        response = self.client.get(
            reverse("api:settings-detail", args=["example-settings"])
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.json()

        self.assertSchema(SettingsSchema, data)

    def test_should_not_retrieve_id_does_not_exist(self):
        response = self.client.get(reverse("api:settings-detail", args=["invalid-key"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_should_not_retrieve_if_not_authenticated(self):
        # clear authorization header
        self.unauthenticated()

        response = self.client.get(
            reverse("api:settings-detail", args=["session-price"])
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
