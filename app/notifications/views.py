from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse

@login_required()
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    response = render(request, 'notifications/pages/notifications.html', {
        'notifications': notifications
    })

    notifications.filter(is_read=False).update(is_read=True)

    return response

@login_required()
def notifications_status(request):
    has_new_notifications = Notification.objects.filter(recipient=request.user,is_read=False).exists()

    return JsonResponse({'has_new_notifications': has_new_notifications})