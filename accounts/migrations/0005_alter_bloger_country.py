# Generated by Django 3.2.5 on 2021-07-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210726_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloger',
            name='country',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Город'),
        ),
    ]