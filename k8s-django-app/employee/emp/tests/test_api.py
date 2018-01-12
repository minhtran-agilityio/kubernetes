import nose.tools as nt
import factory
import json

from django.test import TestCase
from django.core import serializers

from tastypie.test import ResourceTestCaseMixin, TestApiClient

from department.models import Department
from contact.models import Contact
from emp.models import Employee

from emp.apis import EmployeeResource, EmployeeSearchResource
from utils.register_user import register_user

class EmployeeResourceTestCase(ResourceTestCaseMixin):
    def setUp(self):
        super(EmployeeResourceTestCase, self).setUp()

        # Define new account test and create it.
        register_user(self)

        # Define variable to use requests properly
        self.client = TestApiClient()

        # Create and save new department for testing
        self.department_1 = Department.objects.create(name='department_1')

        # Create and save new employee for testing
        self.employee_1 = Employee.objects.create(first_name='John', last_name='Cena', birthday='1964-01-05', email='john.cena@gmail.com', status=1, department=self.department_1)

        # Define api url for get and post method
        self.api_url = '/api/v1/employee/'
        self.api_url_custom = '/api/v1/custom_employee/'

        # Define data for POST method
        self.post_data = {
            'first_name': 'Cori',
            'last_name': 'Lanyon',
            'birthday': '6/28/1909',
            'email': 'clanyonrr@goo.ne.jp',
            'status': 1,
            'department': '/api/v1/department/{0}/'.format(self.department_1.pk)
        }

    def tearDown(self):
        pass

    def get_credentials(self):
        return self.create_basic(username=self.username,
                                 password=self.password)

# Testing method related API of EmployeeResource
class EmployeeAuthenticationTest(EmployeeResourceTestCase, TestCase):
    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.client.get(self.api_url, format='json'))

    def test_get_list_json(self):
        resp = self.client.get(self.api_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_get_list(self):
        get = self.client.get(self.api_url, format='json', authentication=self.get_credentials())

        self.assertHttpOK(get)
        self.assertEqual(Employee.objects.count(), 1)

    def test_post_single(self):
        self.assertEqual(Employee.objects.count(), 1)     # Test number employee before post

        post = self.client.post(self.api_url, format='json', data=self.post_data, authentication=self.get_credentials())

        self.assertHttpCreated(post)
        self.assertEqual(Employee.objects.count(), 2)     # Test number contact after post

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.client.delete(self.api_url, format='json'))

    def test_delete_detail(self):
        self.assertEqual(Employee.objects.count(), 1)

        delete = self.client.delete(self.api_url, format='json', authentication=self.get_credentials())

        self.assertHttpAccepted(delete)
        self.assertEqual(Employee.objects.count(), 0)

    def test_filter_department(self):
        # Create more department and employee to filter
        self.department_2 = Department.objects.create(name='department_2')
        self.assertEqual(Department.objects.count(), 2)

        self.employee_2 = Employee.objects.create(first_name='Bevan', last_name='Polotti', birthday='1985-11-11', email='bpolottirq@ftc.gov', status=1, department=self.department_2)
        self.assertEqual(Employee.objects.count(), 2)

        # Define url filter employee by department
        url_filter = '/api/v1/employee/' + self.department_1.name + '/'

        get = self.client.get(url_filter, format='json', authentication=self.get_credentials())
        data_filterd = self.deserialize(get)

        self.assertHttpOK(get)
        self.assertEqual(data_filterd['objects'][0]['first_name'], 'John')
        self.assertEqual(data_filterd['objects'][0]['last_name'], 'Cena')

    def test_filter_name(self):
        get = self.client.get('/api/v1/employee/?format=json&query=John', format='json', authentication=self.get_credentials())
        self.assertHttpOK(get)
