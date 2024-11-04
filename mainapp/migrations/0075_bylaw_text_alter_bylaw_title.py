# Generated by Django 5.0.6 on 2024-11-03 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0074_scout_resource_bylaw'),
    ]

    operations = [
        migrations.AddField(
            model_name='bylaw',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bylaw',
            name='title',
            field=models.CharField(default='Title', max_length=10000),
            preserve_default=False,
        ),
    ]
