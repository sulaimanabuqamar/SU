# Generated by Django 5.0.7 on 2024-07-15 20:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0003_alter_event_cover"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="news",
            name="published_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
