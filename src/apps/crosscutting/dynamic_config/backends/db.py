from celery.utils.collections import OrderedDict
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from apps.crosscutting.dynamic_config.base import BaseDynamicConfigBackend


class DBDynamicConfigBackend(BaseDynamicConfigBackend):
    def __init__(self, model=None, config=None):
        super().__init__(config=config)
        self._model = model or getattr(settings, "DYNAMIC_CONFIG_MODEL", None)
        self._cached_values = {}

    @property
    def model(self):
        """
        Returns the model class based on the model parameter.

        It can be the model itself or a dotted path.
        """
        _cached_prop = "_cached_model"

        if not hasattr(self, _cached_prop):

            if isinstance(self._model, models.Model):
                # returns the model itself.
                setattr(self, _cached_prop, self._model)

            try:
                model = django_apps.get_model(self._model)

            except (LookupError, AttributeError) as exc:
                raise ImproperlyConfigured(
                    f'Cannot load model "{self._model}".'
                ) from exc

            else:
                setattr(self, _cached_prop, model)

        return getattr(self, _cached_prop)

    def get_queryset(self):
        """
        Return a QuerySet of all model instances of configuration.
        """
        return self.model.objects.all()

    def get_all(self):
        """
        Fetch all settings from the dynamic config module.

        Returns:
            dict<str: any>
        """
        stored_config = dict(self.get_queryset().values_list("key", "value"))

        def get_value_from_key(key, cast=None, default=None):
            if key not in stored_config:
                return default

            return self.to_python(stored_config[key], cast=cast)

        return OrderedDict(
            (
                key,
                get_value_from_key(
                    key, cast=config.get("cast"), default=config.get("default")
                ),
            )
            for key, config in sorted(self._config.items(), key=lambda x: x[0])
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
        if item not in self._cached_values:
            if item not in self._config:
                # do not accept not configured key.
                raise KeyError(
                    f'Key "{item}" was not defined in settings.DYNAMIC_CONFIG.'
                )

            config = self._config[item]
            value = (
                self.get_queryset()
                .filter(key=item)
                .values_list("value", flat=True)
                .first()
            )

            value = self.to_python(value, cast=config.get("cast"))

            if value is not None:
                self._cached_values["key"] = value
                return value

            return config.get("default")

        return self._cached_values[item]

    def set(self, item, value):
        """
        Set a value in the dynamic config.

        Args:
            item (str, required): Item key to store the value.
            value (any, required): Value to be stored.
        """
        self.model.objects.update_or_create(key=item, defaults={"value": value})

        if item in self._cached_values:
            # flush cached value.
            del self._cached_values[item]
