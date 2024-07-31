# Generated by Django 5.0.6 on 2024-07-29 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_user_associated_club_user_associated_faculty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='associated_club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.club'),
        ),
        migrations.AlterField(
            model_name='user',
            name='associated_faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.faculty'),
        ),
        migrations.AlterField(
            model_name='user',
            name='associated_student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.student'),
        ),
        migrations.AlterField(
            model_name='user',
            name='associated_varsity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.varsity'),
        ),
    ]