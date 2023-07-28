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
    path('profile/', views.user_profile, name = 'user_profile'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('otp_validater/', views.otp_validater,name='otp_validater'),
    path('passwordsetter/', views.passwordsetter, name = 'passwordsetter'),
    path('address/',views.address, name = 'address'),
    path('add_address/<int:check>', views.add_address, name = 'add_address'),
    path('edit_address/<int:id>/', views.edit_address, name = 'edit_address'),
    path('delete_adddress/<int:id>', views.delete_address, name = 'delete_address'),
    path('wallet/', views.wallet, name = 'wallet'),
   


]