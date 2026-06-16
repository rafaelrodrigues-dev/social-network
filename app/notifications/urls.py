from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications-list'),
    path('<int:id>/read/', views.mark_notification_as_read, name='mark-as-read'),
    path('<int:id>/delete/', views.delete_notification, name='delete'),
]