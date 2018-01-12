from django.contrib.auth.models import User
from django.db.models import Q
from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.paginator import Paginator
from tastypie.serializers import Serializer

from haystack.query import SearchQuerySet

from .models import Employee
from department.models import Department
from department.apis import DepartmentResource

# from utils.decorators import custom_api

class EmployeeResource(ModelResource):
    department = fields.ForeignKey(DepartmentResource, 'department', full=True)

    def determine_format(self, request):
        return 'application/json'

    class Meta:
        queryset = Employee.objects.all()
        list_allowed_methods = ['get', 'post', 'put', 'delete']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'employee'
        filtering = {
            'first_name': ALL,
            'email': ALL,
            'birthday': ['gte'],
            'department': ALL_WITH_RELATIONS
        }

        ordering = ['first_name']

        authentication = BasicAuthentication()
        authorization = Authorization()

        include_resource_uri = False
        always_return_data = True

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>{0})/(?P<department>\w+)/$".format(self._meta.resource_name),
                self.wrap_view('get_employee'),
                name="api_get_employee"
            ),
        ]

    def get_employee(self, request, **kwargs):
        """ Get employee by department
            Using url follow format: http://localhost:8000/api/v1/employee/{department}/?format=json
        """
        self.method_check(request, ['get'])
        department = Department.objects.get(name=kwargs['department'])

        return EmployeeResource().get_list(request, department=department)

    def apply_filters(self, request, applicable_filters):
        """ Search employee by first_name, last_name, email
            Using url follow format: http://localhost:8000/api/v1/employee/?format=json&query=Minh
        """
        base_object_list = super(EmployeeResource, self).apply_filters(request, applicable_filters)

        query = request.GET.get('query', None)
        filters = {}

        if query:
            qset = (
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
            base_object_list = base_object_list.filter(qset).distinct()

        return base_object_list.filter(**filters).distinct()

class EmployeeSearchResource(ModelResource):
    class Meta:
        queryset = Employee.objects.all()
        resource_name = 'custom_employee'
        authentication = BasicAuthentication()
        authorization = Authorization()
        serializer = Serializer(formats=['json', 'plist'])

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Employee).load_all().auto_query(request.GET.get('q', ''))
        paginator = self._meta.paginator_class(request.GET, sqs,
            resource_uri=self.get_resource_uri(), limit=self._meta.limit,
            max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)

        to_be_serialized = paginator.page()

        bundles = [self.build_bundle(obj=result.object, request=request) for result in to_be_serialized['objects']]
        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

    # =========================================
    # Just comment for create utils custom_api
    # NOT WORK at now.
    # =========================================
    # @custom_api(allowed=['get'])
    # def get_search(self, request, **kwargs):
    #     # Do the query.
    #     sqs = SearchQuerySet().models(employee).load_all().auto_query(request.GET.get('q', ''))
    #     paginator = Paginator(sqs, 20)

    #     try:
    #         page = paginator.page(int(request.GET.get('page', 1)))
    #     except InvalidPage:
    #         raise Http404("Sorry, no results on that page.")

    #     objects = []

    #     for result in page.object_list:
    #         bundle = self.build_bundle(obj=result.object, request=request)
    #         bundle = self.full_dehydrate(bundle)
    #         objects.append(bundle)

    #     return {'objects': objects}
