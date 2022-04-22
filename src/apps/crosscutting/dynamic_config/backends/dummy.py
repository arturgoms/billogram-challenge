from apps.crosscutting.dynamic_config.base import BaseDynamicConfigBackend


class DummyDynamicConfigBackend(BaseDynamicConfigBackend):
    def get_all(self):
        return {
            # always returns default value.
            key: config.get("default")
            for key, config in self._config.items()
        }

    def get(self, item):
        if item not in self._config:
            # do not accept not configured key.
            raise KeyError(f'Key "{item}" was not defined in settings.DYNAMIC_CONFIG.')

        # always returns default value.
        return self._config[item].get("default")

    def set(self, item, value):
        # do nothing.
        pass
