from notifications.models import Notification

def notify(recipient,message,sender=None,title='System'):
    """
    Create a notification for the recipient.
    if sender is None, it defaults to the system.
    """
    notification = Notification.objects.create(
        sender=sender,
        recipient=recipient,
        title=title,
        message=message
    )
    return notification