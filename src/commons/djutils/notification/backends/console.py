import sys
import threading

from commons.djutils.notification.base import (
    BaseNotificationBackend,
    post_notification_sent,
)


class NotificationBackend(BaseNotificationBackend):
    """
    Notification backend that writes messages to console instead of sending them.
    """

    def __init__(self, *args, **kwargs):
        self.stream = kwargs.pop("stream", sys.stdout)
        self._lock = threading.RLock()
        super().__init__(*args, **kwargs)

    def write_message(self, notification, to):
        msg = f"[{to}] {notification.title} - {notification.content}\n"
        msg += "\n".join(
            map(lambda x: "{!r} = {!r}".format(*x), notification.payload.items())
        )
        self.stream.write("%s\n" % msg)
        self.stream.write("-" * 79)
        self.stream.write("\n")

    def send(self, notification):
        """
        Write all messages to the stream in a thread-safe way.
        """
        if not notification:
            return

        msg_count = 0
        with self._lock:
            try:
                stream_created = self.open()  # pylint: disable=E1111

                for recipient in notification.to:
                    self.write_message(notification, recipient)
                    self.stream.flush()  # flush after each message

                    # trigger for post send signal to improve traceability.
                    post_notification_sent.send(
                        notification.clone(to=[recipient], connection=self),
                        success=True,
                        context={},
                    )

                    msg_count += 1

                if stream_created:
                    self.close()

            except Exception:
                if not self.fail_silently:
                    raise

        return msg_count
