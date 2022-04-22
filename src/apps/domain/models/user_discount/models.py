from django.db import models
from commons.models.base import Model
from django.utils.translation import gettext_lazy as _
from apps.domain.models.user_discount.managers import UserDiscountManager


class UserDiscount(Model):
    user = models.ForeignKey(
        'domain.User',
        verbose_name=_('User'),
        related_name='user_discount',
        on_delete=models.CASCADE)

    discount = models.ForeignKey(
        'domain.Discount',
        verbose_name=_('Discount'),
        related_name='user_discount',
        on_delete=models.CASCADE)

    objects = UserDiscountManager()

    class Meta:
        db_table = "user_discount"
        verbose_name = _("User Discount")
        verbose_name_plural = _("User Discounts")
        ordering = ["pk"]

    def __str__(self):
        return str(self.id)
