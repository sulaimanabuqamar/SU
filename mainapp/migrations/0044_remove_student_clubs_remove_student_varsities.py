# Generated by Django 5.0.6 on 2024-09-04 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0043_rename_players_varsity_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='clubs',
        ),
        migrations.RemoveField(
            model_name='student',
            name='varsities',
        ),
    ]