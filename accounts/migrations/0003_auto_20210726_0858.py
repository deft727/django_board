# Generated by Django 3.2.5 on 2021-07-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210726_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloger',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='reader',
            name='of_age',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
