from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminCoupon, name = 'adminCoupon' ),
    path('addcoupon/', views.addCoupon, name = 'addCoupon'),
    path('couponStatus/<int:id>', views.couponStatus, name = 'couponStatus'),
    path('editCoupon/<int:id>', views.editCoupon, name = 'editCoupon'),
    path('applyCoupon/<int:id>', views.applyCoupon, name = 'applyCoupon'),
    
     

]