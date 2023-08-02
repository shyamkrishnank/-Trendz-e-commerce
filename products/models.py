from django.db import models
from category.models import Category

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    price = models.DecimalField(default=0, max_digits=20,decimal_places=2)

    def make_price(self):
        return 0.0

    original_price = models.DecimalField(default= make_price, max_digits=20,decimal_places=2)
    stocks = models.IntegerField(default=0)
    discription = models.TextField(default='NONE')
   
  

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')