# Generated by Django 5.0.6 on 2024-09-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0046_alter_news_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='group',
            field=models.CharField(choices=[('ngr', 'All Year Levels'), ('12', 'Senior'), ('11', 'Junior'), ('10', 'Sophomore'), ('9', 'Freshman')], default='ngr', max_length=3),
        ),
    ]
