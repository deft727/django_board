# Generated by Django 3.2.6 on 2021-08-06 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_rename_avatar_bloger_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reader',
            name='avatar',
        ),
        migrations.AddField(
            model_name='reader',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
