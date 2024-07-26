# Generated by Django 5.0 on 2024-07-16 22:05

import django.db.models.deletion
import mainapp.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("mainapp", "0012_alter_faculty_options_alter_student_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="content_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="club",
            name="object_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="content_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="object_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="news",
            name="content_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="news",
            name="object_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="varsity",
            name="content_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="varsity",
            name="object_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.CreateModel(
            name="Links",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=255)),
                ("link", models.URLField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Socials",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Insta", "Instagram"),
                            ("TT", "TikTok"),
                            ("LI", "LinkedIn"),
                        ],
                        max_length=255,
                    ),
                ),
                ("link", models.URLField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
    ]
