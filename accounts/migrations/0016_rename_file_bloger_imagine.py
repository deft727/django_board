# Generated by Django 3.2.6 on 2021-08-09 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210809_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloger',
            old_name='file',
            new_name='imagine',
        ),
    ]