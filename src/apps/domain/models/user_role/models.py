from django.db import models
from django.utils.translation import gettext_lazy as _

from commons.models.base import Model


class UserRole(Model):
    user = models.ForeignKey(
        "domain.User",
        verbose_name=_("User"),
        related_name="user_roles",
        on_delete=models.CASCADE,
    )

    role = models.CharField(_("Role"), max_length=500, null=True, blank=True)

    class Meta:
        db_table = "user_role"
        verbose_name = _("User Role")
        verbose_name_plural = _("Users Roles")
