from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.domain.models.brand.managers import BrandManager
from commons.models.base import Model


class Brand(Model):

    name = models.CharField(_("Name"), max_length=60)

    website = models.URLField(_("Website"))

    email = models.EmailField(_("Email"))

    objects = BrandManager()

    class Meta:
        db_table = "brand"
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ["website"]

    def __str__(self):
        return self.website
