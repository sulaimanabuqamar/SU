# Generated by Django 5.0.6 on 2024-09-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0037_news_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='awaiting_approval',
            field=models.BooleanField(default=True),
        ),
    ]
