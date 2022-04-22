"""
Django settings for development environment.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from split_settings.tools import include

from settings.base import BASE_DIR
from settings.base import INSTALLED_APPS
from settings.base import MIDDLEWARE

include("base.py")

ROOT_URLCONF = "urls.development"

INSTALLED_APPS += ["silk"]


MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]


# Celery Settings
# http://docs.celeryproject.org/en/5.0/configuration.html

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

CELERY_BROKER_URL = "memory"


# Email Settings
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_HOST

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"

# Media files (Uploaded files)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# Django Silk Settings
# Disable Silk admin tracing.
# Comment this if you want to debug administration panel.
# https://silk.readthedocs.io/en/latest/configuration.html

SILKY_IGNORE_URLS = ["/admin/", "/en-us/admin/", "/pt-br/admin/", "/media/", "/static/"]

SILKY_INTERCEPT_FUNC = lambda request: not any(
    map(request.path.startswith, SILKY_IGNORE_URLS)
)  # noqa

# Conference Client

CONFERENCE_CLIENT = "apps.crosscutting.twilio.conference.dummy.DummyConferenceClient"
CHAT_CLIENT = "apps.crosscutting.twilio.chat.dummy.DummyChatClient"
