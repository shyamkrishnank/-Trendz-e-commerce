import random
import string
from django.db import models
from accounts.models import Users,Address
from products.models import Products

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('wallet_payment','FROM WALLET'),
        ('cash_on_delivery','CASH ON DELIVERY'),
        ('online_payment','ONLINE PAYMENT'),
    )
 

    def generate_order_id():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(10))

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    order_num = models.CharField(max_length=20, default=generate_order_id) 
    payment_type = models.CharField(max_length=100,choices=PAYMENT_CHOICES,default="CASH ON DELIVERY")
    

    @property
    def total_price(self):
        total = 0
        for items in self.orderitems.all():
            total += items.products_price * items.quantity
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
    varient = models.CharField(max_length=30,default='6-10yr')
    products_price = models.DecimalField(default=0, max_digits=20,decimal_places=2)
    quantity = models.IntegerField()
    order_status = models.CharField(max_length=50,choices=order_choices,default='Order Confirmed')
    date_delivered = models.DateTimeField(null=True, blank=True, default=None)

    @property
    def total_price(self):
        total= self.products_price * self.quantity
        return total

class Returned(models.Model):
    def generate_return_id():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(10))
    return_num = models.CharField(max_length=20, default=generate_return_id)
    order = models.ForeignKey(OrderDetail,on_delete=models.CASCADE, related_name='returned')
    reason = models.TextField()
    details = models.TextField(null=True, blank=True, default=None)
    date_submitted = models.DateTimeField(auto_now=True)
    date_returned = models.DateTimeField(null=True, blank=True, default=None)
    
    
