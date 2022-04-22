from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.domain.models.user.managers import UserManager
from commons.functools import cached_property
from commons.models.base import Model


class User(AbstractBaseUser, Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, _("Active")
        BLOCKED = 2, _("Blocked")

    name = models.CharField(_("Name"), max_length=60)

    email = models.EmailField(_("Email"), unique=True)

    date_joined = models.DateField(_("Date Joined"), default=timezone.now)

    status = models.PositiveSmallIntegerField(
        _("Status"), choices=Status.choices, default=Status.ACTIVE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    is_staff = True
    is_superuser = models.BooleanField(_("Is Superuser"), default=False)

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def is_active(self):
        """
        Return whether user is active
        """
        return self.status == User.Status.ACTIVE

    # Permissions

    def has_perm(self, *args, **kwargs):
        return self.is_staff

    def has_perms(self, *args, **kwargs):
        return self.is_staff

    def has_module_perms(self, *args, **kwargs):
        return self.is_staff

    def get_user_permissions(self, *args, **kwargs):
        return []

    def get_group_permissions(self, *args, **kwargs):
        return []

    def get_all_permissions(self, *args, **kwargs):
        return []

    @cached_property
    def roles(self):
        return list(self.user_roles.values_list("role", flat=True))


@receiver(post_migrate)
def create_superuser(sender, *args, **kwargs):
    """
    Add super user on first migration.
    """
    if sender.label == User._meta.app_label and not User.objects.exists():
        # create super user with project settings information.
        User.objects.create_superuser(
            name=getattr(settings, "SUPERUSER_NAME"),
            email=getattr(settings, "SUPERUSER_EMAIL"),
            password=getattr(settings, "SUPERUSER_PASSWORD"),
        )
