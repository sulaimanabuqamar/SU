from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_alumni',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='graduation_year',
            field=models.CharField(blank=True, help_text='Academic year e.g. 2024-2025', max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='archived_year',
            field=models.CharField(blank=True, help_text='Academic year when archived e.g. 2024-2025', max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='archived_year',
            field=models.CharField(blank=True, help_text='Academic year when archived e.g. 2024-2025', max_length=11, null=True),
        ),
    ]
