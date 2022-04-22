"""
src URL Configuration for development environment.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import path, include

from commons.admin.utils import admin_url_pattern

urlpatterns = [
    path("", include("urls.base")),
    path("silk/", include("silk.urls", namespace="silk")),
]

urlpatterns += i18n_patterns(
    path(admin_url_pattern(), include("apps.admin.urls")),
    path("", include("commons.admin.urls")),
)

# Apply the media and static files urls.
# It works only when is in debug mode.
urlpatterns += static(
    settings.STATIC_URL, document_root=getattr(settings, "STATIC_ROOT")
)
urlpatterns += static(settings.MEDIA_URL, document_root=getattr(settings, "MEDIA_ROOT"))
