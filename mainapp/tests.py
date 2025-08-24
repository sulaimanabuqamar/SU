from django.test import TestCase
from mainapp.models import Student
from mainapp.views import bulk_grade_update_logic

class BulkGradeUpdateTest(TestCase):
    def setUp(self):
        Student.objects.create(student_db_id='1', year_level=11, section='A')
        Student.objects.create(student_db_id='2', year_level=12, section='B')
        Student.objects.create(student_db_id='3', year_level=9, section='C')
        Student.objects.create(student_db_id='4', year_level=None, section='D')

    def test_bulk_grade_update(self):
        updated, deleted = bulk_grade_update_logic()
        students = Student.objects.all()
        # Student 1: 11 -> 12 (updated)
        # Student 2: 12 -> 13 (deleted)
        # Student 3: 9 -> 10 (updated)
        # Student 4: None -> None (not updated)
        self.assertEqual(updated, 2)
        self.assertEqual(deleted, 1)
        self.assertEqual(students.count(), 3)
        self.assertTrue(Student.objects.filter(student_db_id='1', year_level=12).exists())
        self.assertTrue(Student.objects.filter(student_db_id='3', year_level=10).exists())
        self.assertTrue(Student.objects.filter(student_db_id='4').exists())
        self.assertFalse(Student.objects.filter(student_db_id='2').exists())
