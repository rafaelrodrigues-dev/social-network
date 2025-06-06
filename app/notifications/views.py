from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required()
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    response = render(request, 'notifications/pages/notifications.html', {
        'notifications': notifications
    })

    notifications.filter(is_read=False).update(is_read=True)

    return response