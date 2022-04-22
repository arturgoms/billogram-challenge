"""
Django settings for production environment.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import decouple
from split_settings.tools import include

from settings.base import BASE_DIR

include("base.py")


# Decouple Config
# https://github.com/henriquebastos/python-decouple

config = decouple.AutoConfig(BASE_DIR.parent)

# Change this to your domain
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://localhost:1337"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = config("DJANGO_STATIC_ROOT", default="/storage/static/")
STATIC_URL = config("DJANGO_STATIC_URL", default="/static/")


# Media files (Uploaded files)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_ROOT = config("DJANGO_MEDIA_ROOT", default="/storage/media/")
MEDIA_URL = config("DJANGO_MEDIA_URL", default="/media/")
