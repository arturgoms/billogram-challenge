from commons.djutils.notification.base import get_connection, Notification


def send_topic_notification(
    title, content, recipient_list, payload=None, fail_silently=False, connection=None
):
    """
    Easy wrapper for sending a single topic notification to a recipient list.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the Notification class directly.
    """
    connection = connection or get_connection()

    notification = Notification(
        title,
        content,
        to=recipient_list,
        payload=payload,
        connection=connection,
        type=Notification.TOPIC,
    )

    return notification.send(fail_silently=fail_silently)


def send_device_notification(
    title, content, recipient_list, payload=None, fail_silently=False, connection=None
):
    """
    Easy wrapper for sending a single device notification to a recipient list.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the Notification class directly.
    """
    connection = connection or get_connection()

    notification = Notification(
        title,
        content,
        to=recipient_list,
        payload=payload,
        connection=connection,
        type=Notification.DEVICE,
    )

    return notification.send(fail_silently=fail_silently)
