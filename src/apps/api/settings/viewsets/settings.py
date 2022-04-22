from commons.djutils.api.pagination import SkipPagination
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.api.settings.serializers.settings import SettingsSerializer
from apps.crosscutting.dynamic_config import dynamic_config
from commons.api import viewsets


class SettingsViewSet(viewsets.GenericViewSet):
    serializer_class = SettingsSerializer
    pagination_class = SkipPagination
    lookup_url_kwarg = "key"
    lookup_value_regex = r"([\w-]+)"

    def list(self, request, *args, **kwargs):
        data = list(
            map(
                lambda x: {"key": x[0], "value": x[1]}, dynamic_config.get_all().items()
            )
        )
        serializer = self.get_serializer(data, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        key = self.kwargs.get(self.lookup_url_kwarg)

        try:
            value = dynamic_config[key]

        except KeyError as exc:
            raise NotFound() from exc

        serializer = self.get_serializer({"key": key, "value": value})
        return Response(serializer.data, status=status.HTTP_200_OK)
