# Generated by Django 4.2.3 on 2023-08-03 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_varient_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='varient',
            field=models.CharField(choices=[('1-3yr', 'XS'), ('3-5yr', 'XM'), ('6-8yr', 'MS'), ('9-12yr', 'ML'), ('12-15yr', 'L')], default='6-8yr', max_length=20),
        ),
        migrations.DeleteModel(
            name='Varient',
        ),
    ]
