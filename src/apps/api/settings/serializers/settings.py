from rest_framework import serializers

from commons.api.serializers import Serializer


class SettingsSerializer(Serializer):
    key = serializers.CharField()
    value = serializers.SerializerMethodField(method_name="_get_value")

    def _get_value(self, item):
        """
        Retrieve value from item.
        """
        return item.get("value")
