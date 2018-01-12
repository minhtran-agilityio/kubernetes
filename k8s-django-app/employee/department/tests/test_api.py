import nose.tools as nt
import factory

from django.test import TestCase

from tastypie.test import ResourceTestCaseMixin, TestApiClient

from department.models import Department
from department.apis import DepartmentResource
from utils.register_user import register_user

class DepartmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.Sequence(lambda n: "Department #%s" % n)

# Testing method related API of DepartmentResource
class DepartmentResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(DepartmentResourceTest, self).setUp()

        # Define new account test and create it.
        register_user(self)

        # Define variable to use requests properly
        self.client = TestApiClient()

        # Create and save a new department
        self.department_1 = DepartmentFactory.create()

        # Define api url for get and post method
        self.api_url = '/api/v1/department/'

        # Define data for POST method
        self.post_data = {
            'name': 'test department'
        }

    def tearDown(self):
        Department.objects.all().delete()

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_get_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.client.get(self.api_url, format='json'))

    def test_get_list_json(self):
        resp = self.client.get(self.api_url, format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

    def test_get_list(self):
        get = self.client.get(self.api_url, format='json', authentication=self.get_credentials())

        self.assertHttpOK(get)
        self.assertEqual(Department.objects.count(), 1)

    def test_post_single(self):
        self.assertEqual(Department.objects.count(), 1)     # Test number department before post

        post = self.client.post(self.api_url, format='json', data=self.post_data, authentication=self.get_credentials())

        self.assertHttpCreated(post)
        self.assertEqual(Department.objects.count(), 2)     # Test number department after post

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.client.delete(self.api_url, format='json'))

    def test_delete_detail(self):
        self.assertEqual(Department.objects.count(), 1)

        delete = self.client.delete(self.api_url, format='json', authentication=self.get_credentials())

        self.assertHttpAccepted(delete)
        self.assertEqual(Department.objects.count(), 0)

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(self.client.put(self.api_url, format='json', data={}))

    def test_update_detail(self):
        api_update = '/api/v1/department/1/'
        original_data = self.deserialize(self.client.get(api_update, format='json', authentication=self.get_credentials()))

        new_data = original_data.copy()
        new_data['name'] = 'Name A'

        self.assertEqual(Department.objects.count(), 1)
        self.assertHttpAccepted(self.client.put(api_update, format='json', data=new_data, authentication=self.get_credentials()))

        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(Department.objects.count(), 1)

        # Check for updated data.
        self.assertEqual(Department.objects.get(id=1).name, 'Name A')
