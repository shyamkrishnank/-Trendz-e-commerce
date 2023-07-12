from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns=[
    
    path('', views.home, name = 'home'),
    path('login/', views.login, name ='user_login'),
    path('signup/', views.signup, name = 'user_signup'),
    path('otp_validate/', views.otp_validate, name='otp_validate'),
    path('products<int:id>/', views.products, name='products'),
    path('product_detail<int:id>/', views.product_detail, name = 'product_detail'),
    path('user_logout', views.logout, name='user_logout'),


]