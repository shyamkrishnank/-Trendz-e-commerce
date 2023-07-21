from django.urls import path
from . import views

urlpatterns = [

    path('', views.order, name = 'order'),
    path('ordersuccess/<str:id>', views.ordersuccess, name='ordersuccess'),
    path('orderpage/',views.orderpage,name = 'orderpage'),
    path('orderdetails/<int:id>',views.orderdetails, name = 'orderdetails'),
    path('adminorder/', views.adminOrders, name = 'adminorder'),
    path('adminorderdetail/<int:id>',views.adminOrderDetail, name = 'adminorderdetails'),
    path('status_change/<int:id>', views.status_change, name = 'statuschange'),
    path('cancel_order/<int:id>', views.order_cancel, name = 'cancel_order')
   
]
