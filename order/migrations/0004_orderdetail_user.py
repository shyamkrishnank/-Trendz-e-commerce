# Generated by Django 4.2.3 on 2023-07-19 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_cartitems_cart_remove_cartitems_products_and_more'),
        ('order', '0003_alter_orderdetail_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.users'),
        ),
    ]