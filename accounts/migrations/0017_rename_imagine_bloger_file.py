# Generated by Django 3.2.6 on 2021-08-09 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_rename_file_bloger_imagine'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloger',
            old_name='imagine',
            new_name='file',
        ),
    ]
