from django.http import Http404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification
from django.http import HttpResponse


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/pages/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)

def mark_notification_as_read(request, id):
    if request.method != 'POST':
        raise Http404()
    notification = Notification.objects.get(id=id)
    notification.is_read = True
    notification.save()
    return HttpResponse(status=200)

def delete_notification(request, id):
    if request.method != 'POST':
        raise Http404()
    notification = Notification.objects.get(id=id)
    notification.delete()
    return HttpResponse(status=204)