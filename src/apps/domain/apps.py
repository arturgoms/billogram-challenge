from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DomainConfig(AppConfig):
    name = "apps.domain"
    verbose_name = _("Domain")
