# Generated by Django 5.0.6 on 2024-10-22 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0066_meeting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='heads_only',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='leadership_only',
        ),
    ]
