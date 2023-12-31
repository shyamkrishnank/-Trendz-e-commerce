# Generated by Django 4.2.3 on 2023-08-09 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='max_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='coupon',
            name='min_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
