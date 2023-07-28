from django.db import models
from django.contrib.auth.models import User
from products.models import Products
# Create your models here.
class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='c_user')
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)

class Address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='address')
    fullname = models.CharField(max_length=255,default="NULL")
    address1 = models.CharField(max_length=255,default="NULL")
    city = models.CharField(max_length=255,default="NULL")
    state = models.CharField(max_length=255,default="NULL")
    postalcode = models.CharField(max_length=10,default="NULL")
    country = models.CharField(max_length=255,default="NULL")
    current = models.BooleanField(default=False,)
    active = models.BooleanField(default=True)

class Wallet(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='wallet')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


