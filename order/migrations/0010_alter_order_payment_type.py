# Generated by Django 4.2.3 on 2023-07-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('debit_credit_card', 'DEBIT/CREDIT CARD'), ('cash_on_delivery', 'CASH ON DELIVERY'), ('online_payment', 'Online Payment')], default='CASH ON DELIVERY', max_length=100),
        ),
    ]
