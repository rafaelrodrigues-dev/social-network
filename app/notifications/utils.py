from notifications.models import Notification

def notify(recipient, text, sender=None, notification_type=None, publication=None) -> None:
    Notification.objects.create(
        recipient=recipient,
        text=text,
        sender=sender,
        notification_type=notification_type,
        publication=publication
    )