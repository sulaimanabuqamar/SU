# Generated by Django 5.0.6 on 2024-11-03 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0077_club_bylaws'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='type',
            field=models.CharField(choices=[('link', 'Website Link'), ('file', 'Uploaded File')], default='file', max_length=20),
            preserve_default=False,
        ),
    ]
