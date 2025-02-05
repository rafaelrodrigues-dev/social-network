from django.urls import path
from publications import views

app_name = 'publications'

urlpatterns = [
    path('',views.home,name='home')
]