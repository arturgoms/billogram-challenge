import math
import re

import dateutil.parser
from commons.utils import parser


def date(value):
    """Returns a date instance from value."""
    return dateutil.parser.parse(value).date()


def datetime(value):
    """Returns a datetime instance from value."""
    return dateutil.parser.parse(value)


def time_to_seconds(value):
    """
    Convert HH:MM:SS or HH:MM string pattern to seconds.
    """
    if not bool(re.match(r"^(\d+):(\d{1,2})(:(\d{1,2}))?$", value)):
        raise ValueError("Invalid value '{}'".format(value))

    parts = map(int, value.split(":"))
    multipliers = (3600, 60, 1)
    return sum(map(math.prod, zip(parts, multipliers)))


def time_from_seconds(value):
    """
    Convert seconds integer to string pattern HH:MM:SS.
    """
    min_, sec = divmod(value, 60)
    hour, min_ = divmod(min_, 60)
    return "%02d:%02d:%02d" % (hour, min_, sec)


def parse_safe(value, cast=lambda x: x, default=None):
    """
    Parse a value in a safe way by returning
    a default value instead of raise
    an exception.
    """
    try:
        value = parser.parse(value, cast=cast)

    except (TypeError, ValueError):
        return default

    else:
        return value
