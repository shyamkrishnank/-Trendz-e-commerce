from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns=[
    
     path('', views.products, name='products'),
     path('product_details<int:id>/', views.product_details, name = 'product_details'),
     path('add_product/', views.add_product, name='add_product'),
     path('delete_product<int:id>', views.delete_product, name = 'delete_product'),
     path('edit_product<int:id>/', views.edit_product, name = 'edit_product')
     
     


]