# Generated by Django 5.0.6 on 2024-09-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0061_homepage_carousel_scroll_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
