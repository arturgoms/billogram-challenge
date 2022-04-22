from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):  # noqa
        tz = request.META.get("HTTP_ACCEPT_TIMEZONE") or settings.TIME_ZONE
        timezone.activate(tz)
