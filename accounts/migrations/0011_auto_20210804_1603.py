# Generated by Django 3.2.6 on 2021-08-04 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210804_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloger',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='reader',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Avatar',
        ),
    ]
