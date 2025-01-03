# Generated by Django 5.0.6 on 2024-10-24 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0070_remove_meeting_attending_faculty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='type',
            field=models.CharField(choices=[('boys', 'Boys Only'), ('girls', 'Girls Only'), ('mixed', 'Mixed Club')], default='mixed', max_length=6),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10),
        ),
    ]
