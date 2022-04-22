from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import set_rollback


def exception_handler(exc, *args, **kwargs):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    elif isinstance(exc, ValidationError) and hasattr(exc, "message_dict"):
        exc = exceptions.ValidationError(exc.message_dict)

    elif isinstance(exc, ValidationError) and not hasattr(exc, "message_dict"):
        exc = exceptions.ValidationError(exc.messages)

    if isinstance(exc, exceptions.APIException):
        headers = {}
        auth_header = getattr(exc, "auth_header", None)
        wait = getattr(exc, "wait", None)

        if auth_header is not None:
            headers["WWW-Authenticate"] = auth_header

        if wait:
            headers["Retry-After"] = "%d" % wait

        if isinstance(exc.detail, list):
            data = [{"field": api_settings.NON_FIELD_ERRORS_KEY, "errors": exc.detail}]

        elif isinstance(exc.detail, dict):
            data = [
                {"field": field, "errors": errors}
                for field, errors in exc.detail.items()
            ]

        else:
            data = {"detail": exc.detail}

        if exc.status_code == status.HTTP_400_BAD_REQUEST:
            data = {"detail": exc.default_detail, "errors": data}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
