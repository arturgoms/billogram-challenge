import os
import uuid

from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify


@deconstructible
class filename_builder:  # noqa
    """
    Build a generic filename based on instance model.
    """

    def __init__(self, *path):
        self.path = path
        self.upload_path = getattr(settings, "UPLOAD_PATH", None) or ""

    def __call__(self, instance, filename):
        opts = getattr(instance, "_meta")

        path = os.path.join(
            *list(
                map(
                    lambda x: x if not callable(x) else x(instance),
                    self.path or [opts.app_label, opts.model_name],
                )
            )
        )

        filename, ext = os.path.splitext(filename)
        return os.path.join(
            self.upload_path, path, f"{uuid.uuid4()}-{slugify(filename)}{ext}"
        )
