from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.domain.models.discount.managers import DiscountManager
from commons.models.base import Model


class Discount(Model):

    code = models.CharField(_("Code"), max_length=60)

    description = models.CharField(_("Description"), max_length=60)

    quantity = models.PositiveIntegerField(
        _('Quantity'), help_text=_(
            'Total that can be used'
        ))

    hide = models.BooleanField(
        _('Hide'), default=False)

    enable = models.BooleanField(
        _('Enable'), default=True)

    brand = models.ForeignKey(
        'domain.Brand',
        verbose_name=_('Brand'),
        related_name='brand_discount',
        on_delete=models.CASCADE)

    objects = DiscountManager()

    class Meta:
        db_table = "discount"
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")
        ordering = ["code"]

    def __str__(self):
        return self.code


