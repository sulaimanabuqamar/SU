from django.db import migrations, models


def forwards(apps, schema_editor):
    Student = apps.get_model('mainapp', 'Student')
    User = apps.get_model('mainapp', 'User')
    Club = apps.get_model('mainapp', 'Club')

    for student in Student.objects.filter(is_alumni=True):
        try:
            # associated_student is a FK from User -> Student; associated_student_id holds the Student PK
            user = User.objects.filter(associated_student_id=student.pk).first()
        except Exception:
            user = None
        archived = []
        if user is not None:
            for club in Club.objects.all():
                roles = []
                try:
                    if user in club.heads.all():
                        roles.append('head')
                except Exception:
                    pass
                try:
                    if user in club.leadership.all():
                        roles.append('leadership')
                except Exception:
                    pass
                try:
                    if user in club.advisors.all():
                        roles.append('advisor')
                except Exception:
                    pass
                try:
                    if user in club.members.all():
                        roles.append('member')
                except Exception:
                    pass

                if roles:
                    # remove roles
                    try:
                        if 'member' in roles:
                            club.members.remove(user)
                    except Exception:
                        pass
                    try:
                        if 'head' in roles:
                            club.heads.remove(user)
                    except Exception:
                        pass
                    try:
                        if 'leadership' in roles:
                            club.leadership.remove(user)
                    except Exception:
                        pass
                    try:
                        if 'advisor' in roles:
                            club.advisors.remove(user)
                    except Exception:
                        pass

                    try:
                        if club in user.associated_clubs.all():
                            user.associated_clubs.remove(club)
                    except Exception:
                        pass

                    archived.append({'id': club.id, 'roles': roles})
            try:
                user.save()
            except Exception:
                pass

        # persist the removed club ids and roles on the student
        try:
            student.archived_club_ids = archived
            student.save()
        except Exception:
            pass


def reverse(apps, schema_editor):
    # no-op reverse: we don't automatically restore memberships on migration rollback
    return


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_add_archivestate'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='archived_club_ids',
            field=models.JSONField(blank=True, null=True, default=list, help_text='List of club IDs the student was removed from when archived'),
        ),
        migrations.RunPython(forwards, reverse),
    ]
