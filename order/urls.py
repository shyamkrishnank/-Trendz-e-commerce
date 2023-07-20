from django.urls import path
from . import views

urlpatterns = [

    path('', views.order, name = 'order'),
    path('ordersuccess/<str:id>', views.ordersuccess, name='ordersuccess'),
    path('orderpage/',views.orderpage,name = 'orderpage'),
    path('orderdetails/<int:id>',views.orderdetails, name = 'orderdetails'),
   
]
