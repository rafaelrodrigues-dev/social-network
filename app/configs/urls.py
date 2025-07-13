from django.urls import path
from . import views

app_name = 'configs'

urlpatterns = [
    path('', views.ConfigsView.as_view(), name='configs'),
    path('edit/',views.EditAuthorView.as_view(),name='edit_author')
]