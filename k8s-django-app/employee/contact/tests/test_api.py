import nose.tools as nt
import factory

from django.test import TestCase

from tastypie.test import ResourceTestCaseMixin, TestApiClient

from department.models import Department
from contact.models import Contact
from emp.models import Employee

from contact.apis import ContactResource
from utils.register_user import register_user

class ContactResourceTestCase(ResourceTestCaseMixin):
    def setUp(self):
        super(ContactResourceTestCase, self).setUp()

        # Define new account test and create it.
        register_user(self)

        # Define variable to use requests properly
        self.client = TestApiClient()

        # Create and save new department for testing
        self.department_1 = Department.objects.create(name='department_1')

        # Create and save new employee for testing
        self.employee_1 = Employee.objects.create(first_name='John', last_name='Cena', birthday='1964-01-05', email='john.cena@gmail.com', status=1, department=self.department_1)

        # Create and save new contact for testing
        self.contact_1 = Contact.objects.create(name='contact_1', employee=self.employee_1)

        # Define api url for get and post method
        self.api_url = '/api/v1/contact/'

        # Define data for POST method
        self.post_data = {
            'name': 'test contact',
            'employee': '/api/v1/employee/{0}/'.format(self.employee_1.pk)
        }

    def tearDown(self):
        Contact.objects.all().delete()

    def get_credentials(self):
        return self.create_basic(username=self.username,
                                 password=self.password)

# Testing method related API of ContactResource
class ContactAuthenticationTest(ContactResourceTestCase, TestCase):
    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.client.get(self.api_url, format='json'))

    def test_get_list_json(self):
        resp = self.client.get(self.api_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_get_list(self):
        get = self.client.get(self.api_url, format='json', authentication=self.get_credentials())

        self.assertHttpOK(get)
        self.assertEqual(Contact.objects.count(), 1)

    def test_post_single(self):
        self.assertEqual(Contact.objects.count(), 1)     # Test number contact before post

        post = self.client.post(self.api_url, format='json', data=self.post_data, authentication=self.get_credentials())

        self.assertHttpCreated(post)
        self.assertEqual(Contact.objects.count(), 2)     # Test number contact after post

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.client.delete(self.api_url, format='json'))

    def test_delete_detail(self):
        self.assertEqual(Contact.objects.count(), 1)

        delete = self.client.delete(self.api_url, format='json', authentication=self.get_credentials())

        self.assertHttpAccepted(delete)
        self.assertEqual(Contact.objects.count(), 0)
