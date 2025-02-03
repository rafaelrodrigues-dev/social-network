from django.urls import path
from publications import views

urlpatterns = [
    path('',views.home,name='home')
]