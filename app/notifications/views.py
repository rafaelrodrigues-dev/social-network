from django.http import Http404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/pages/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)

@require_POST
@login_required
def mark_notification_as_read(request, id):
    notification = get_object_or_404(Notification, id=id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return HttpResponse(status=200)

@require_POST
@login_required
def delete_notification(request, id):
    notification = get_object_or_404(Notification, id=id, recipient=request.user)
    notification.delete()
    return HttpResponse(status=204)