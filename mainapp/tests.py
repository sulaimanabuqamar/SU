from django.test import TestCase
from mainapp.models import Student, User, News, Event, Club
from mainapp.views import bulk_grade_update_logic, get_graduation_academic_year_for_student


class ArchiveGraduatesTest(TestCase):
    def setUp(self):
        club = Club.objects.create(name='Test Club', about='About', logo='default-pfp.png', color='#000000')
        # create students
        s1 = Student.objects.create(student_db_id='1', year_level=11, section='A')
        s2 = Student.objects.create(student_db_id='2', year_level=12, section='B')
        s3 = Student.objects.create(student_db_id='3', year_level=9, section='C')
        # create users tied to students
        u1 = User.objects.create(email='u1@example.com', name='U1')
        u1.associated_student = s1
        u1.save()
        u2 = User.objects.create(email='u2@example.com', name='U2')
        u2.associated_student = s2
        u2.save()
        # news by u2 and an event attended by u2
        News.objects.create(author=u2, cover='default-pfp.png', title='News', text='n', summary='s')
        e = Event.objects.create(author=club, title='Event', text='e', summary='s', date='2025-01-01')
        e.attending_Students.add(u2)

    def test_archive_flow(self):
        updated, archived_students, archived_events, archived_news = bulk_grade_update_logic()
        s2 = Student.objects.get(student_db_id='2')
        expected = get_graduation_academic_year_for_student(s2)
        self.assertTrue(updated >= 2)
        self.assertTrue(s2.is_alumni)
        self.assertEqual(s2.graduation_year, expected)
        self.assertTrue(News.objects.filter(archived_year=expected).exists())
        self.assertTrue(Event.objects.filter(archived_year=expected).exists())
