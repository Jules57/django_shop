# Generated by Django 4.2.6 on 2023-10-26 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_purchase_time_purchase_bought_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='return',
            old_name='return_time',
            new_name='returned_at',
        ),
    ]
