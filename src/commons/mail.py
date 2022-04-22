from django.conf import settings
from django.core import mail
from django import template as django_template
from django.utils import timezone as django_tz
from django.utils.html import strip_tags

from commons.timezone import timezone


def send_mail(subject, template, to, from_email=None, context=None, tz=None):
    """
    Send template email shortcut.

    Args:
        subject (string, required): Email subject.
        template (string, required): Path to email template.
        to (list, required): Email or list of recipients.
        from_email (str, required): From email.
        context (dict, optional): Extra data for the Message.
        tz (str, optional): Timezone to render template.
    """
    context = context or {}

    with timezone(tz or django_tz.get_current_timezone()):

        # render a html message.
        html_message = (
            django_template.engines["django"]
            .get_template(template_name=template)
            .render(context=context)
        )

        # render subject
        subject = (
            django_template.engines["django"]
            .from_string(template_code=subject)
            .render(context=context)
        )

    mail.send_mail(
        subject=subject,
        html_message=html_message,
        message="\n\n".join(
            filter(None, map(lambda x: x.strip(), strip_tags(html_message).split("\n")))
        ),
        from_email=from_email or getattr(settings, "DEFAULT_FROM_EMAIL"),
        recipient_list=[to] if not isinstance(to, (list, tuple)) else to,
    )


class TemplateEmailSender:
    is_enabled = True

    def get_context(self, **context):
        """
        Returns the context to the email.

        Args:
            **context (dict, optional): Email rendering context.

        Returns:
            dict
        """
        return context

    def send_email(self, subject, template, to, tz=None):
        """
        Send email if enabled.

        Args:
            subject (str, required): Email subject.
            template (str, required): Email template path.
            to (list<str>, required): Email receiver.
            tz (str, optional): Timezone to render the email.
        """
        if self.is_enabled is True:
            # only send if enabled
            send_mail(
                subject=subject,
                template=template,
                to=to,
                tz=tz,
                context=self.get_context(),
            )

    def send(self):
        """
        Send the email by applying custom rules.
        """
        raise NotImplementedError()
