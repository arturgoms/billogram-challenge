import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from pytz import InvalidTimeError
from rest_framework import serializers


class TimestampField(serializers.Field):
    default_error_messages = {
        "invalid": _(
            "Datetime has wrong format. Use one of these formats instead: {format}."
        ),
        "make_aware": _('Invalid datetime for the timezone "{timezone}".'),
        "overflow": _("Datetime value out of range."),
    }

    def __init__(self, *args, default_timezone=None, **kwargs):
        self._timezone = default_timezone
        super().__init__(*args, **kwargs)

    @property
    def timezone(self):
        if not settings.USE_TZ:
            return None

        return self._timezone or timezone.get_current_timezone()

    def enforce_timezone(self, value):
        """
        When `self.timezone` is `None`, always return naive datetimes.
        When `self.timezone` is not `None`, always return aware datetimes.
        """
        timezone_ = self.timezone

        try:

            if timezone_ and timezone.is_aware(value):
                value = value.astimezone(timezone_)

            elif timezone_ and not timezone.is_aware(value):
                value = timezone.make_aware(value, timezone_)

            elif not timezone_ and timezone.is_aware(value):
                value = timezone.make_naive(value, timezone.utc)

        except InvalidTimeError:
            self.fail("make_aware", timezone=timezone_)

        except OverflowError:
            self.fail("overflow")

        return value

    def _from_timestamp(self, value):
        """
        Value from timestamp.
        """
        try:
            values = float(value), float(value) / 1e3

        except (TypeError, ValueError):
            return None

        for val in values:
            try:
                return datetime.datetime.utcfromtimestamp(val)

            except (TypeError, ValueError):
                continue

        return None

    def to_internal_value(self, data):
        if not data:
            return None

        if isinstance(data, datetime.datetime):
            return self.enforce_timezone(data)

        value = self._from_timestamp(data)

        if not value:
            self.fail("invalid")

        return self.enforce_timezone(value)

    def to_representation(self, value):
        if not value:
            return None

        value = self.enforce_timezone(value)
        return datetime.datetime.timestamp(value)
