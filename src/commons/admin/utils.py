from django.conf import settings
from django.utils.module_loading import import_string


def call_from_string(path, *args, **kwargs):
    """
    Returns a result from a function.
    """
    try:
        result = import_string(path)

        if callable(result):
            # try to call the function and
            # return the result.
            return result(*args, **kwargs)

        return result
    except ImportError:
        return False


def admin_url_pattern(path=None):
    """
    Returns admin url based on settings.
    """
    admin_url_prefix = getattr(settings, "ADMIN_SITE_URL_PREFIX", None) or "/admin/"
    output = [admin_url_prefix.rstrip("/").lstrip("/")]

    if path:
        output.append(path.rstrip("/").lstrip("/"))

    return "%s/" % "/".join(output)
