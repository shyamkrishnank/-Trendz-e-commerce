from django.db import models
from accounts.models import Users
from accounts.models import Address
from products.models import Products


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        total = 0
        for items in self.cartitems.all():
            total += items.products.price * items.quantity
        return total


class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='cartitems')
    products = models.ForeignKey(Products,related_name="products", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def product_total(self):
        total = self.products.price * self.quantity
        return total
    