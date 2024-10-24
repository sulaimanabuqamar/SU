# Generated by Django 5.0.6 on 2024-09-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0047_alter_news_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='grade',
            field=models.CharField(choices=[('nosec', 'All Sections'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J')], default='nosec', max_length=5),
        ),
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.CharField(choices=[('ngr', 'All Year Levels'), ('12', 'Senior'), ('11', 'Junior'), ('10', 'Sophomore'), ('9', 'Freshman')], default='ngr', max_length=3),
        ),
    ]
