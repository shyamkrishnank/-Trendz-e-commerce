# Generated by Django 4.2.3 on 2023-08-10 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_orderdetail_varient'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='payed_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
