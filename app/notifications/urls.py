from django.urls import path
from . import views

urlpatterns = [
    path('',views.notifications,name='notifications'),
    path('status/',views.notifications_status,name='notifications_status'),
]