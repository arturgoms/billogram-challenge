from django.conf import settings as django_settings


# Django admin shortcuts

ADMIN_SHORTCUTS = getattr(django_settings, "ADMIN_SHORTCUTS", None)


# User Links

ADMIN_USER_LINKS = getattr(django_settings, "ADMIN_USER_LINKS", None)
