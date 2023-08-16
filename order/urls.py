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
    path('cancel_order/<int:id>', views.order_cancel, name = 'cancel_order'),
    path('orderfilter/', views.filter, name= 'filter'),
    path('return_reason/<int:id>', views.return_reason, name = 'return_reason'),
    path('returnconfirmation/', views.return_confirmation, name = 'return_confirmation'),
    path('report/', views.report, name = 'report'),
    path('reportFilter/',views.report_filter, name = 'reportFilter'),
    path('report_download/', views.report_download, name = 'reportDownload'),
    path('invoice/<int:id>', views.invoice, name = 'invoice'),
   
]
