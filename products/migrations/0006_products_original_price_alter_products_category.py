# Generated by Django 4.2.3 on 2023-07-30 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('products', '0005_products_discription'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='original_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='category.category'),
        ),
    ]
