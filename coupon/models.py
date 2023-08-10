from django.db import models

# Create your models here.
class Coupon(models.Model):
    name = models.CharField(max_length=30)
    coupon_code = models.CharField(max_length=15)
    discount = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True, default=None)
    end_date = models.DateField(null=True, blank=True, default=None)
    min_rate = models.DecimalField(default=0, max_digits=20,decimal_places=2)
    max_rate = models.DecimalField(default=0, max_digits=20,decimal_places=2)
    is_active = models.BooleanField(default=False)

