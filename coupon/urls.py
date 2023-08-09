from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminCoupon, name = 'adminCoupon' ),
    
     

]