from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.domain.models.user.managers import UserManager
from commons.models.base import Model


class User(Model):
    first_name = models.CharField(_("First Name"), max_length=60)

    last_name = models.CharField(_("Last Name"), max_length=60)

    email = models.EmailField(_("Email"))

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["first_name"]

    @property
    def full_name(self):
        """
        Returns student fullname.
        """
        return " ".join([self.first_name, self.last_name])

    def __str__(self):
        return self.full_name
