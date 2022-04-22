from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from commons.mail import send_mail


def send_user_invite_email(user, password):
    """
    Send user invite email.

    Args:
        user (domain.User, required): Invited user.
        password (str, required): Invited user's password.
    """
    subject = _("Panel Access")

    send_mail(
        subject=subject,
        template="email/user/invite.html",
        to=user.email,
        context={
            "subject": subject,
            "user": user,
            "password": password,
            "primary_button": {
                "text": _("Access My Account"),
                "url": reverse("admin:index"),
            },
        },
    )


def send_new_password_email(user, password):
    """
    Send user new password email.

    Args:
        user (domain.User, required): Invited user.
        password (str, required): Invited user's password.
    """
    subject = _("Panel Access")

    send_mail(
        subject=subject,
        template="email/user/new_password.html",
        to=user.email,
        context={
            "subject": subject,
            "user": user,
            "password": password,
            "primary_button": {
                "text": _("Access My Account"),
                "url": reverse("admin:index"),
            },
        },
    )
