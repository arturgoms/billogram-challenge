from commons.djutils.notification.base import BaseNotificationBackend


class NotificationBackend(BaseNotificationBackend):
    """
    Notification backend that does nothing with messages instead of sending them.
    """

    def send(self, notification):
        return len(notification.to)
