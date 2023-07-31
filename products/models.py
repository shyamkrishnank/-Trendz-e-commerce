from django.db import models
from category.models import Category

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    price = models.FloatField(default=0)

    def make_price(self):
        return self.price

    original_price = models.FloatField(default= make_price)
    stocks = models.IntegerField(default=0)
    discription = models.TextField(default='NONE')
   
  

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')