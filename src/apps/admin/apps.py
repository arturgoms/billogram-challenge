from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminConfig(AppConfig):
    name = "apps.admin"
    label = "administration"
    verbose_name = _("Admin")
