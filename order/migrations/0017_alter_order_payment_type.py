# Generated by Django 4.2.3 on 2023-07-28 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_returned_return_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('wallet_payment', 'FROM WALLET'), ('cash_on_delivery', 'CASH ON DELIVERY'), ('online_payment', 'ONLINE PAYMENT')], default='CASH ON DELIVERY', max_length=100),
        ),
    ]
