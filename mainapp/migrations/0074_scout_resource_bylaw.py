# Generated by Django 5.0.6 on 2024-11-03 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0073_event_draft_meeting_draft_news_draft'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scout',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('mainapp.club',),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10000)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.links')),
            ],
        ),
        migrations.CreateModel(
            name='Bylaw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('resources', models.ManyToManyField(blank=True, related_name='bylaw_resources', to='mainapp.resource')),
            ],
        ),
    ]