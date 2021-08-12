# Generated by Django 3.2.6 on 2021-08-11 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0017_rename_imagine_bloger_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloger',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader', to=settings.AUTH_USER_MODEL, verbose_name='читатель'),
        ),
    ]