import random
import string
from django.db import models
from accounts.models import Users,Address
from products.models import Products

class Order(models.Model):
 

    def generate_order_id():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(10))

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    order_num = models.CharField(max_length=20, default=generate_order_id) 
     

    @property
    def total_price(self):
        total = 0
        for items in self.orderitems.all():
            total += items.products.price * items.quantity
        return total
    

class OrderDetail(models.Model): 
    order_choices= (
        ('order_confirmed','Order Confirmed'),
        ('order_cancelled','Order Cancelled'),
        ('order_pending','Order Pending'),
        ('order_deliverd','Order Delivered'),
        ('order_shipped','Order Shipped'),
        ('order_outofdelivery','Order Out of Delivery'),
        ('order_returned','Order Returned'),

    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_status = models.CharField(max_length=50,choices=order_choices,default='Order Confirmed')

    @property
    def total_price(self):
        total= self.products.price * self.quantity
        return total
    
