# Generated by Django 4.0.8 on 2024-04-15 19:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_alter_uploadedfile_options_uploadedfile_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
