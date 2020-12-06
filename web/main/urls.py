from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
  path('', views.index, name='index'),
  path('post/<int:pk>/', views.post_detail, name='post_detail'),
]