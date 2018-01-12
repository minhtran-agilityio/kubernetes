import time

from django.contrib.auth.models import User
from django.db.models import signals

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from .models import Department

class DepartmentResource(ModelResource):
    class Meta:
        queryset = Department.objects.all()
        list_allowed_methods = ['get', 'post', 'put', 'delete']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'department'
        include_resource_uri = False

        authentication = BasicAuthentication()
        authorization = Authorization()

    def dehydrate_name(self, bundle):
        return bundle.data['name'].upper()

    def dehydrate(self, bundle):
        bundle.data["server_time"] = time.ctime()
        return bundle
