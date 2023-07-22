from django.urls import path
from . import views

urlpatterns = [

    path('', views.cart, name = 'cart'),
    path('add_cart/<int:id>',views.add_cart, name='add_cart'),
    path('add_cart1/<int:id>',views.add_cart1, name='add_cart1'),
    path('removecart/<int:id>',views.remove_cartitem, name='remove_cartitem'),
    path('quantity_increment/<int:id>', views.quantity_increment, name = 'quantity_increment'),
    path('quantity_decrement/<int:id>' ,views.quantity_decrement, name='quantity_decrement' ),
    path('checkout/', views.checkout, name = 'checkout'),
    path('add_address/', views.add_checkout_address, name = 'addcheckoutaddress')
   
]
