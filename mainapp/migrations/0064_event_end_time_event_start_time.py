# Generated by Django 5.0.6 on 2024-10-10 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0063_event_confirmed_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]