# Generated by Django 3.2.6 on 2021-08-05 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20210803_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]
