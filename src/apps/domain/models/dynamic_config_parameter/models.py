from django.db import models
from django.utils.translation import gettext_lazy as _

from commons.models import Model


class DynamicConfigParameter(Model):

    key = models.CharField(_("Key"), max_length=100, unique=True)

    value = models.TextField(_("Value"), null=True)

    class Meta:
        db_table = "dynamic_config_parameter"
        verbose_name = _("Dynamic Config Parameter")
        verbose_name_plural = _("Dynamic Config Parameters")
        ordering = ["created_at"]

    def __str__(self):
        return self.key
