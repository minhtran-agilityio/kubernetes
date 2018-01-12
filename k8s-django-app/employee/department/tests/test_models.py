from django.test import TestCase
from department.models import Department

class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department_test = Department.objects.create(name='department test')

    def tearDown(self):
        pass

    def test_string_representation(self):
        department = Department(name="Department string")
        self.assertEqual(str(department), department.name)

    def test_department_name(self):
        self.assertEqual(self.department_test.name, 'department test')

    def test_label_name(self):
        field_name = self.department_test._meta.get_field('name').verbose_name
        self.assertEqual(field_name, 'name')

    def test_length_field(self):
        length = self.department_test._meta.get_field('name').max_length
        self.assertEqual(length, 60)
