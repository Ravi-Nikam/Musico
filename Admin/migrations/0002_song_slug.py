# Generated by Django 5.0.1 on 2024-01-19 20:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
    ]
