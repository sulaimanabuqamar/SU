# Generated by Django 5.0.6 on 2024-09-02 10:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0039_news_denied_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attending_Students',
            field=models.ManyToManyField(blank=True, related_name='attending_students', to=settings.AUTH_USER_MODEL),
        ),
    ]
