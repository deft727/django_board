# Generated by Django 3.2.6 on 2021-08-05 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_rename_avatar_jpeg_photo_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='photo',
        ),
        migrations.AddField(
            model_name='photo',
            name='file',
            field=models.ImageField(default=1, upload_to='photos/'),
            preserve_default=False,
        ),
    ]
