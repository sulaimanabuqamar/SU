# Generated by Django 5.0.6 on 2024-09-02 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0038_news_awaiting_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='denied_reason',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
