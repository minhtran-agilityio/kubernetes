from django.contrib.auth.models import User
from django.db.models import signals

from tastypie import fields
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']

        authentication = ApiKeyAuthentication()
        authorization = Authorization()
