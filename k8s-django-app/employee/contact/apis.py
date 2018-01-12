from django.db.models import signals

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from .models import Contact
from emp.apis import EmployeeResource

class ContactResource(ModelResource):
    employee = fields.ForeignKey(EmployeeResource, 'employee', full=True)

    class Meta:
        queryset = Contact.objects.all()
        list_allowed_methods = ['get', 'post', 'put', 'delete']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'contact'

        authentication = BasicAuthentication()
        authorization = Authorization()
