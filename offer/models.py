import random
import string
from django.db import models
from accounts.models import Users
from category.models import Category


# Create your models here.
class Offer(models.Model):
    def generate_order_id():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(6))
    
    offer_num = models.CharField(max_length=10,default=generate_order_id)
    name = models.CharField(max_length=50)
    discount = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True, default=None)
    end_date = models.DateField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=False)
    discription = models.TextField(null=True, blank=True, default=None)

class OfferCategory(models.Model):
    offer = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name='categoryEligible')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)