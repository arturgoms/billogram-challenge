from typing import Sequence

from django.conf import settings
from django.dispatch import Signal
from django.utils.module_loading import import_string


# IMPORTANT: Backends could trigger this signal to perform
# additional actions to the notifications, such as logging.
post_notification_sent = Signal()


def get_connection(backend=None, fail_silently=False, **kwargs):
    """
    Load a notification backend and return an instance of it.

    If backend is None (default), use settings.NOTIFICATION_BACKEND.

    Both fail_silently and other keyword arguments are used in the
    construction of the backend.
    """
    cls = import_string(backend or settings.NOTIFICATION_BACKEND)
    return cls(fail_silently=fail_silently, **kwargs)


class Notification:
    """
    Generic notification representation.

    Attributes:
         title (str, required): Notification title.
         content (str, required): Notification content.
         payload (mapping, required): Key value structure containing
            values to be sent into the payload.
         to (sequence, required): List of topics or tokens to deliver the notification.
         type (str, required): Define notification type. Values: device, topic.
         connection (NotificationBackend, optional): Connection to be used to send notification.
            If not defined will use the settings.NOTIFICATION_BACKEND value.
    """

    DEVICE = "device"
    TOPIC = "topic"

    def __init__(
        self, title="", content="", payload=None, to=None, type=None, connection=None
    ):  # noqa
        if to:
            assert isinstance(to, Sequence), '"to" argument must be a sequence'
            self.to = list(to)
        else:
            self.to = []

        assert type in {
            Notification.DEVICE,
            Notification.TOPIC,
        }, f'"type" argument accept only {Notification.DEVICE} or {Notification.TOPIC} values.'

        self.title = title
        self.content = content
        self.payload = payload or {}
        self.type = type
        self.connection = connection

    def __repr__(self):
        return f"Notification('{self.title}', '{self.content}', {self.payload!r}, {self.to!r}, '{self.type}')"

    def get_connection(self, fail_silently=False):
        """Returns the connection to send the notification."""
        if not self.connection:
            self.connection = get_connection()
        self.connection.fail_silently = fail_silently
        return self.connection

    def send(self, fail_silently=False):
        """Send the email message."""
        if not self.to:
            # Don't bother creating the network connection if there's nobody to
            # send to.
            return 0

        return self.get_connection(fail_silently).send(self)

    def clone(self, **update):
        """
        Returns a copy of current object by applying updates.
        """
        return Notification(
            **{
                "title": self.title,
                "content": self.content,
                "payload": self.payload,
                "to": self.to,
                "type": self.type,
                "connection": self.connection,
                **update,
            }
        )


class BaseNotificationBackend:
    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently

    def open(self):
        """
        Open a network connection.

        This method can be overwritten by backend implementations to
        open a network connection.

        It's up to the backend implementation to track the status of
        a network connection if it's needed by the backend.

        This method can be called by applications to force a single
        network connection to be used when sending notifications.

        The default implementation does nothing.
        """
        pass

    def close(self):
        """
        Close a network connection.
        """
        pass

    def __enter__(self):
        try:
            self.open()

        except Exception:
            self.close()
            raise

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def send(self, notification):
        """
        Send one Notification object and return the number of notifications sent.
        """
        raise NotImplementedError(
            "subclasses of BaseNotificationBackend must override send() method"
        )
