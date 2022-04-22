"""
Django settings for src project.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import decouple

from split_settings.tools import include

from settings.base import BASE_DIR, DATABASES

include("base.py")


# Decouple Config
# https://github.com/henriquebastos/python-decouple

config = decouple.AutoConfig(BASE_DIR.parent)


# Database settings
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DATABASE-TEST

DATABASES["default"]["TEST"] = {"NAME": config("DATABASE_TEST_NAME", "_test")}


# Celery Settings
# http://docs.celeryproject.org/en/5.0/configuration.html

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = False

CELERY_BROKER_URL = "memory"


# Email Settings
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_HOST

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Authentication Client

AUTHENTICATION_CLIENT = "commons.tests.auth.TestAuthenticationClient"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_test/"


# Media files (Uploaded files)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media_test/"


# Dynamic Config

DYNAMIC_CONFIG_BACKEND = (
    "apps.crosscutting.dynamic_config.backends.dummy.DummyDynamicConfigBackend"
)


# Conference Client

CONFERENCE_CLIENT = "apps.crosscutting.twilio.conference.dummy.DummyConferenceClient"
CHAT_CLIENT = "apps.crosscutting.twilio.chat.dummy.DummyChatClient"
NOTIFICATION_BACKEND = (
    "apps.websocket.notification.backend.dummy.DummyNotificationBackend"
)


# Hotmart
# https://app-vlc.hotmart.com/tools/webhook

HOTMART_WEBHOOK_HOTTOK = "1234"
