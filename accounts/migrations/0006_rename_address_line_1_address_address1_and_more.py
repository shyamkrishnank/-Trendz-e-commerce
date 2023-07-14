# Generated by Django 4.2.3 on 2023-07-14 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_address_address_address_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line_1',
            new_name='address1',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='full_name',
            new_name='fullname',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='postal_code',
            new_name='postalcode',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_line_2',
        ),
    ]
