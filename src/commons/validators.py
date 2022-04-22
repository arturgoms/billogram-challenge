from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


class RuleValidator:
    message = _("Invalid Value.")
    code = "invalid"

    def __init__(self, rule, message=None):
        assert callable(rule), "Argument rule must be a callable."

        self.rule = rule
        self.message = message or self.message

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {"value": cleaned}

        if not self.rule(cleaned):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return (
            self.rule == other.rule
            and self.message == other.message
            and self.code == other.code
        )

    def clean(self, value):
        return value


@deconstructible
class FileSizeValidator:
    message = _(
        'File Size "%(current_size)s" is not allowed. ' "Allowed size %(max_size)s."
    )
    code = "limit_value"

    def __init__(self, max_size, message=None):
        self.max_size = max_size
        if message:
            self.message = message

    def __call__(self, value):
        current_size = value.size

        info = {
            "current_size": f"{current_size} Bytes",
            "max_size": f"{self.max_size} Bytes",
        }

        if current_size > self.max_size:
            raise ValidationError(self.message, code=self.code, params=info)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.max_size == other.max_size
            and self.message == other.message
            and self.code == other.code
        )


@deconstructible
class ImageResolutionValidator:
    message = _(
        'Image resolution "%(current_resolution)s" is not allowed. '
        "Allowed resolutions are: %(allowed_resolutions)s."
    )

    code = "invalid"

    def __init__(self, allowed_resolutions, message=None):
        self.allowed_resolutions = allowed_resolutions

        if message:
            self.message = message

    def __call__(self, value):
        if not value:
            # ignore for None.
            return

        width, height = get_image_dimensions(value)

        info = {
            "current_resolution": f"{width}x{height}px",
            "allowed_resolutions": ", ".join(
                [f"{w}x{h}px" for w, h in self.allowed_resolutions]
            ),
        }

        if not width or not height:
            # if is not image return ignore.
            raise ValidationError(self.message, code=self.code, params=info)

        if not list(
            filter(lambda x: width == x[0] and height == x[1], self.allowed_resolutions)
        ):
            raise ValidationError(self.message, code=self.code, params=info)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return (
            self.allowed_resolutions == other.allowed_resolutions
            and self.message == other.message
            and self.code == other.code
        )
