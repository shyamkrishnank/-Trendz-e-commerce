# Generated by Django 4.2.3 on 2023-07-29 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('offer', '0002_offer_discription'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='category_eligible',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='category.category'),
        ),
    ]
