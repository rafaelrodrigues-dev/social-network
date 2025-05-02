from django.urls import path
from publications import views

app_name = 'publications'

urlpatterns = [
    path('',views.home,name='home'),
    path('p/<int:pk>/',views.publication_detail,name='publication-detail'),
    path('p/<int:pk>/like/',views.like,name='like'),
    path('p/<int:pk>/comment/',views.comment,name='comment'),
    path('p/<int:pk>/delete/',views.delete_publication,name='delete-publication'),
    path('search/',views.search,name='search')
]