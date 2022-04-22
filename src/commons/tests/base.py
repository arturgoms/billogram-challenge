import json
from shutil import rmtree
from unittest.util import safe_repr

import jsonschema
from django.conf import settings
from django.test.testcases import TestCase as BaseTestCase
from mixer.backend.django import mixer
from rest_framework.test import APITestCase as BaseAPITestCase

from commons.tests.faker import faker


class TestCase(BaseTestCase):
    # Faker support
    # https://github.com/joke2k/faker
    # Providers: https://github.com/joke2k/faker/tree/master/faker/providers
    faker = faker

    # Mixer support
    # https://github.com/klen/mixer
    mixer = mixer

    @classmethod
    def tearDownClass(cls):
        """
        Cleanup media files storage.
        """
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)


class APITestCase(BaseAPITestCase):
    # Faker support
    # https://github.com/joke2k/faker
    # Providers: https://github.com/joke2k/faker/tree/master/faker/providers
    faker = faker

    # Mixer support
    # https://github.com/klen/mixer
    mixer = mixer

    @classmethod
    def tearDownClass(cls):
        """
        Cleanup media files storage.
        """
        super().tearDownClass()
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    # pylint: disable=invalid-name
    def assertSchema(self, schema, data):
        """
        Check that data is valid for schema.
        """
        data, schema = dict(data), dict(schema)

        try:
            jsonschema.validate(data, schema=schema)

        except jsonschema.ValidationError:
            self.fail(
                "\nThe Value: \n{data} \n\nIs not valid for schema: \n{schema}".format(
                    data=json.dumps(data, indent=2),
                    schema=json.dumps(schema, indent=2),
                )
            )

    # pylint: disable=invalid-name
    def assertPaginatedSchema(self, schema, data):
        """
        Check that data is valid for schema.
        """
        self.assertSchema(
            {
                "type": "object",
                "properties": {
                    "count": {"type": "integer"},
                    "next": {"type": ["string", "null"], "format": "uri"},
                    "previous": {"type": ["string", "null"], "format": "uri"},
                    "results": {"type": "array", "items": dict(schema)},
                },
                "required": ["count", "next", "previous", "results"],
                "additionalProperties": False,
            },
            data,
        )

    # pylint: disable=invalid-name
    def assertListSchema(self, schema, data):
        """
        Check that data is valid for schema.
        """
        self.assertSchema(
            {
                "type": "object",
                "properties": {"results": {"type": "array", "items": dict(schema)}},
                "required": ["results"],
                "additionalProperties": False,
            },
            data,
        )

    # pylint: disable=invalid-name
    def assertAny(self, func, container):
        """
        Check that at least one item match in container.
        """
        if not any(func(item) for item in container):
            self.fail("No items have matched in %s" % safe_repr(container))

    # pylint: disable=invalid-name
    def assertNotAny(self, func, container):
        """
        Check that no items match in container.
        """
        if any(func(item) for item in container):
            self.fail("Any items have matched in %s" % safe_repr(container))

    # pylint: disable=invalid-name
    def assertAll(self, func, container):
        """
        Check that all items match in container.
        """
        if not all(func(item) for item in container):
            self.fail(
                "There where items that has not matched in %s" % safe_repr(container)
            )

    # pylint: disable=invalid-name
    def assertNotAll(self, func, container):
        """
        Check that all items does not match in container.
        """
        if all(func(item) for item in container):
            self.fail("All items has matched in %s" % safe_repr(container))

    # pylint: disable=invalid-name
    def assertExists(self, func, container):
        """
        Check that item exists in container.
        """
        count = len(list(filter(func, container)))

        if count == 0:
            self.fail(
                "%s items found in container with given expression." % safe_repr(count)
            )

    # pylint: disable=invalid-name
    def assertNotExists(self, func, container):
        """
        Check that item does not exist in container.
        """
        count = len(list(filter(func, container)))

        if count != 0:
            self.fail(
                "%s items found in container with given expression." % safe_repr(count)
            )

    # pylint: disable=invalid-name
    def assertIsEmpty(self, container):
        """
        Check whether the container is empty.
        """
        if not len(container) == 0:
            self.fail("%s != %s" % (len(container), 0))

    # pylint: disable=invalid-name
    def assertIsNotEmpty(self, container):
        """
        Check whether the container is not empty.
        """
        if not len(container) != 0:
            self.fail("%s == %s" % (len(container), 0))
