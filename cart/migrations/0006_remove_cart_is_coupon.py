# Generated by Django 4.2.3 on 2023-08-10 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cart_is_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_coupon',
        ),
    ]
