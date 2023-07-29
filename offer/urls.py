from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminOffer, name = 'adminoffer' ),
    path('addoffer/', views.addOffer, name='addOffer'),
    path('offerstatus/<int:id>',views.offerStatus, name = 'offerstatus')
     

]