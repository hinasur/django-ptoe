from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
  path('', views.index, name='index'),
  path('upload/', views.UploadView.as_view(), name='upload'),
  path('list/', views.ListView.as_view(), name='list'),
  path('dell_file/', views.dell_file, name='dell_file'),
]