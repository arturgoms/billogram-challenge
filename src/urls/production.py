"""
src URL Configuration for production environment.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include

from commons.admin.utils import admin_url_pattern

urlpatterns = [path("", include("urls.base"))]

urlpatterns += i18n_patterns(
    path(admin_url_pattern(), include("apps.admin.urls")),
    path("", include("commons.admin.urls")),
)
