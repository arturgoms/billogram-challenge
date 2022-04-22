from django.conf import settings
from django.utils.module_loading import import_string


def get_dynamic_config_backend(backend=None):
    """
    Load a dynamic config backend and return an instance of it.
    If backend is None (default), use settings.DYNAMIC_CONFIG_BACKEND.
    """
    cls = import_string(backend or settings.DYNAMIC_CONFIG_BACKEND)

    return cls()


dynamic_config = get_dynamic_config_backend()
