from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminConfig(AppConfig):
    name = "commons.admin"
    label = "base_administration"
    verbose_name = _("Admin")
