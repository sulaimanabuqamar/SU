# Generated by Django 5.0.6 on 2024-09-13 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0058_user_associated_scouts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='associated_scouts',
        ),
        migrations.AlterField(
            model_name='homepage',
            name='event_highlight_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_event_highlight_1', to='mainapp.event'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='event_highlight_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_event_highlight_2', to='mainapp.event'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='event_highlight_3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_event_highlight_3', to='mainapp.event'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='news_highlight_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_news_highlight_1', to='mainapp.news'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='news_highlight_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_news_highlight_2', to='mainapp.news'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='news_highlight_3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_news_highlight_3', to='mainapp.news'),
        ),
        migrations.DeleteModel(
            name='Scouts',
        ),
    ]
