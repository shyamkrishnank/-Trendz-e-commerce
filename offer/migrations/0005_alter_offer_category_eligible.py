# Generated by Django 4.2.3 on 2023-07-29 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('offer', '0004_remove_offer_category_eligible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='category_eligible',
            field=models.ManyToManyField(to='category.category'),
        ),
    ]
