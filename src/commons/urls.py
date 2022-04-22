from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

from django.conf import settings
from urllib.parse import unquote


def querystring(url, includes=None, excludes=None):
    """
    Handle urls adding or excluding querystring parameters.
    """
    url = urlparse(url)
    query = parse_qs(url.query)
    includes = includes or {}
    excludes = excludes or []

    # apply includes
    query.update(includes)

    # apply excludes
    query = {key: value for key, value in query.items() if key not in excludes}

    # update url
    url = urlunparse(url._replace(query=urlencode(query, True)))  # noqa

    return unquote(url)


def get_absolute_uri(url, request=None, domain=None):
    """
    Returns an absolute url for a given url.
    """
    if not request:
        domain = ((domain or getattr(settings, "DOMAIN", "")) or "").rstrip("/")

        url = url.lstrip("/")

        # resolve the absolute path based in the domain
        # variable if request is missing.
        return f"{domain}/{url}"

    return request.build_absolute_uri(url)
