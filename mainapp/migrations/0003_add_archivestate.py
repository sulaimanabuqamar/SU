from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_add_archive_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_academic_start', models.IntegerField(help_text='Calendar year used as the base for the next archive run (e.g. 2024)')),
            ],
        ),
    ]
