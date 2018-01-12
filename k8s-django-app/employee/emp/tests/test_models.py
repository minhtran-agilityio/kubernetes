from django.test import TestCase

from department.models import Department
from contact.models import Contact
from emp.models import Employee

class ContactTestCase():
    def setUp(self):
        # Create and save new department for testing
        self.department_1 = Department.objects.create(name='department_1')

        # Create and save new employee for testing
        self.employee_1 = Employee.objects.create(first_name='John', last_name='Cena', birthday='1964-01-05', email='john.cena@gmail.com', status=1, department=self.department_1)

    def tearDown(self):
        Department.objects.all().delete()
        Employee.objects.all().delete()

class ContactModelTest(ContactTestCase, TestCase):
    def test_string_representation(self):
        employee = Employee(first_name='John', last_name='Cena')
        self.assertEqual(str(employee), ' '.join([employee.first_name, employee.last_name]))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Employee._meta.verbose_name_plural), "employees")

    def test_department_created(self):
        self.assertEqual(self.employee_1.first_name, 'John')
        self.assertEqual(self.employee_1.last_name, 'Cena')
        self.assertEqual(self.employee_1.birthday, '1964-01-05')
        self.assertEqual(self.employee_1.email, 'john.cena@gmail.com')
        self.assertEqual(self.employee_1.status, 1)

    def test_labels_name(self):
        first_name = self.employee_1._meta.get_field('first_name').verbose_name
        last_name = self.employee_1._meta.get_field('last_name').verbose_name
        birthday = self.employee_1._meta.get_field('birthday').verbose_name
        email = self.employee_1._meta.get_field('email').verbose_name
        status = self.employee_1._meta.get_field('status').verbose_name
        department = self.employee_1._meta.get_field('department').verbose_name

        self.assertEqual(first_name, 'first name')
        self.assertEqual(last_name, 'last name')
        self.assertEqual(birthday, 'birthday')
        self.assertEqual(email, 'email')
        self.assertEqual(status, 'status')
        self.assertEqual(department, 'department')

    def test_length_fields(self):
        length_first_name = self.employee_1._meta.get_field('first_name').max_length
        length_last_name = self.employee_1._meta.get_field('last_name').max_length
        length_email = self.employee_1._meta.get_field('email').max_length
        
        self.assertEqual(length_first_name, 20)
        self.assertEqual(length_last_name, 20)
        self.assertEqual(length_email, 254)
