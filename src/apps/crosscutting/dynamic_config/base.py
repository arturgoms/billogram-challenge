"""
Supports Dynamic Config feature to be extended.
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from commons.utils import parser


class BaseDynamicConfigBackend:
    def __init__(self, config=None):
        self._config = config or dict(
            map(
                lambda x: (x["key"], x),
                (config or getattr(settings, "DYNAMIC_CONFIG", None)) or [],
            )
        )

    def to_python(self, value, cast=None):
        """
        Cast a value to it's python representation based on the cast function.

        Args:
            value (any, required): Value to be cast.
            cast (func, optional): Function to parse the value. If not provided the value itself will be returned.

        Returns:
            any
        """
        if not cast:
            # no cast required.
            return value

        if not callable(cast):
            # do not accept not callable casters.
            raise ImproperlyConfigured("cast must be a callable.")

        try:
            value = parser.parse(value, cast)

        except (TypeError, ValueError):
            return None

        else:
            return value

    def get_all(self):
        """
        Fetch all settings from the dynamic config module.

        Returns:
            dict<str: any>
        """
        raise NotImplementedError(
            "subclasses of BaseDynamicConfigClient must provide a get_all() method"
        )

    def get(self, item):
        """
        Fetch a given key from the dynamic config. If the key does not exist, return
        default, which itself defaults to None.

        The value will be cast based on project settings.

        Args:
            item (str, required): Item key to retrieve the value.

        Returns:
            any
        """
        raise NotImplementedError(
            "subclasses of BaseDynamicConfigClient must provide a get() method"
        )

    def set(self, item, value):
        """
        Set a value in the dynamic config.

        Args:
            item (str, required): Item key to store the value.
            value (any, required): Value to be stored.
        """
        raise NotImplementedError(
            "subclasses of BaseDynamicConfigClient must provide a set() method"
        )

    def __getitem__(self, item):
        """
        Returns the value for a given key.

        Allows the usage directly by the key:

        >>> from apps.crosscutting.dynamic_config import dynamic_config
        >>> dynamic_config['key']
        """
        return self.get(item=item)
