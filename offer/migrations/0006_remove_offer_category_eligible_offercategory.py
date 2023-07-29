# Generated by Django 4.2.3 on 2023-07-29 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('offer', '0005_alter_offer_category_eligible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='category_eligible',
        ),
        migrations.CreateModel(
            name='OfferCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_eligible', to='offer.offer')),
            ],
        ),
    ]
