# Generated by Django 4.2.3 on 2023-08-04 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_alter_orderdetail_products_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='varient',
            field=models.CharField(default='6-10yr', max_length=30),
        ),
    ]