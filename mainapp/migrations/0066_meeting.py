# Generated by Django 5.0.6 on 2024-10-22 15:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0065_event_published_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='event_covers/')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(blank=True, default='')),
                ('summary', models.CharField(max_length=150)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('location', models.CharField(max_length=150)),
                ('group', models.CharField(choices=[('ngr', 'All Year Levels'), ('12', 'Senior'), ('11', 'Junior'), ('10', 'Sophomore'), ('9', 'Freshman')], default='ngr', max_length=3)),
                ('grade', models.CharField(choices=[('nosec', 'All Sections'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J')], default='nosec', max_length=5)),
                ('heads_only', models.BooleanField(default=False)),
                ('leadership_only', models.BooleanField(default=False)),
                ('attending_Students', models.ManyToManyField(blank=True, related_name='meeting_attending_students', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_meetings', to='mainapp.club')),
                ('links', models.ManyToManyField(blank=True, related_name='emeeting_links', to='mainapp.links')),
            ],
        ),
    ]
