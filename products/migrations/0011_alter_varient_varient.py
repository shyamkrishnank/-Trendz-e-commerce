# Generated by Django 4.2.3 on 2023-08-03 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_varient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='varient',
            name='varient',
            field=models.CharField(choices=[('Medium', 'M'), ('Small', 'S'), ('Large', 'L')], max_length=20),
        ),
    ]
