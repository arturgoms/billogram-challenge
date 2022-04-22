from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AlreadyExistsValidationError(ValidationError):
    def __init__(self, *args, message=None, **kwargs):
        message = message or _('Invalid transaction id "{value}" - already exists.')
        super().__init__(message, *args, **kwargs)
