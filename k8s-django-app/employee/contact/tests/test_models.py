from django.test import TestCase

from department.models import Department
from contact.models import Contact
from emp.models import Employee

class ContactModelTest(TestCase):
    def setUp(self):
        # Create and save new department for testing
        self.department_1 = Department.objects.create(name='department_1')

        # Create and save new employee for testing
        self.employee_1 = Employee.objects.create(first_name='John', last_name='Cena', birthday='1964-01-05', email='john.cena@gmail.com', status=1, department=self.department_1)

        # Create and save new contact for testing
        self.contact_1 = Contact.objects.create(name='contact_1', employee=self.employee_1)

    def tearDown(self):
        pass

    def test_string_representation(self):
        contact = Contact(name='Contact String')
        self.assertEqual(str(contact), contact.name)

    def test_department_name(self):
        self.assertEqual(self.contact_1.name, 'contact_1')

    def test_label_name(self):
        field_name = self.contact_1._meta.get_field('name').verbose_name
        self.assertEqual(field_name, 'name')

        field_employee  = self.contact_1._meta.get_field('employee').verbose_name
        self.assertEqual(field_employee, 'employee')

    def test_length_field(self):
        length = self.contact_1._meta.get_field('name').max_length
        self.assertEqual(length, 60)
