from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditModel(models.Model):

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True
