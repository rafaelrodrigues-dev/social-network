from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('edit/',views.EditProfileView.as_view(),name='edit_profile'),
    path('<str:username>/',views.profile_detail,name='profile'),
    path('<str:username>/follow',views.follow,name='follow'),
]