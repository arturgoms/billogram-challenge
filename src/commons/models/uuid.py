import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDModel(models.Model):

    id = models.UUIDField(_("Id"), default=uuid.uuid4, primary_key=True, editable=False)

    class Meta:
        abstract = True
