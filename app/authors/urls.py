from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
   path('register/',views.register_view,name='register'),
   path('register/create/',views.register_create,name='register_create'),
   path('login/',views.login_view,name='login'),
   path('login/create',views.login_create,name='login_create'),
   path('logout/',views.logout_view,name='logout'),
   path('edit/',views.EditAuthorView.as_view(),name='edit_author')
]
