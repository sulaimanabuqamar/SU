# Generated by Django 5.0.6 on 2024-12-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0087_event_hos_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='hos_approved',
            field=models.BooleanField(default=False),
        ),
    ]