# Generated by Django 3.2.12 on 2024-05-06 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_auto_20240506_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='uploadedfile',
            name='sender',
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
