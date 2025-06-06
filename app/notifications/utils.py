from notifications.models import Notification

def notify(sender,recipient,title,message):
    """
    Create a notification for the recipient.
    """
    notification = Notification.objects.create(
        sender=sender,
        recipient=recipient,
        title=title,
        message=message
    )
    return notification