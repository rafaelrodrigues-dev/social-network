from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('edit/',views.EditProfileView.as_view(),name='edit_profile'),
    path('<str:username>/',views.profile_detail,name='profile'),
    path('<str:username>/follow',views.follow,name='follow'),
    path('<str:username>/new-publication',views.new_publication,name='new_publication'),
    path('<str:username>/new-publication/create',views.new_publication_create,name='new_publication_create'),
]