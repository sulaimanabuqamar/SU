# Generated by Django 5.0.6 on 2024-09-13 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0059_remove_user_associated_scouts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='event_highlight_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_event_highlight_1', to='mainapp.event'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='event_highlight_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_event_highlight_2', to='mainapp.event'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='event_highlight_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_event_highlight_3', to='mainapp.event'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='news_highlight_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_news_highlight_1', to='mainapp.news'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='news_highlight_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_news_highlight_2', to='mainapp.news'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='news_highlight_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_news_highlight_3', to='mainapp.news'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='officer_highlight_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_officer_highlight_1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='officer_highlight_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_officer_highlight_2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='officer_highlight_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_officer_highlight_3', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='officer_highlight_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_officer_highlight_4', to=settings.AUTH_USER_MODEL),
        ),
    ]
