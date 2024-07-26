# Generated by Django 5.0 on 2024-07-16 21:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("mainapp", "0010_alter_varsity_events"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="faculty",
            options={"verbose_name": "Faculty", "verbose_name_plural": "Faculties"},
        ),
        migrations.AlterModelOptions(
            name="student",
            options={"verbose_name": "Student", "verbose_name_plural": "Students"},
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_admin",
        ),
        migrations.AddField(
            model_name="faculty",
            name="department",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="faculty",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="faculty_profiles/"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Designates that this user has all permissions without explicitly assigning them.",
                verbose_name="superuser status",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="clubs",
            field=models.ManyToManyField(
                blank=True, related_name="student_clubs", to="mainapp.club"
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="student_profiles/"
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="section",
            field=models.CharField(
                blank=True,
                choices=[
                    ("A", "A"),
                    ("B", "B"),
                    ("C", "C"),
                    ("D", "D"),
                    ("E", "E"),
                    ("F", "F"),
                    ("G", "G"),
                    ("H", "H"),
                    ("I", "I"),
                ],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="varsities",
            field=models.ManyToManyField(
                blank=True, related_name="student_varsities", to="mainapp.varsity"
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="year_level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "Freshman"),
                    ("SO", "Sophomore"),
                    ("JR", "Junior"),
                    ("SR", "Senior"),
                ],
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=255, unique=True, verbose_name="email address"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=128, verbose_name="password"),
        ),
    ]
