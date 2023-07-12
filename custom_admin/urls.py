from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns=[
    
     path('', views.login, name='admin_login'),
     # dashbord--------------------
     path('home/', views.home, name = 'admin_home'),
     # users-----------------------
     path('users/', views.users, name='users'),
     path('delete_user<int:id>/', views.delete_user, name='delete_user'),
     path('user_active<int:id>/', views.user_active, name = 'user_active'),
     path('admin_logout', views.admin_logout, name = 'admin_logout'),
  


]