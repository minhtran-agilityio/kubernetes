from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from emp.models import Employee
from department.models import Department

class DepartmentEmployeeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('department')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'department'

# Register model to admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'birthday', 'email', 'status', 'department')
    ordering = ['first_name']
    list_filter  = ('department', 'status' ,)
    search_fields = ['email', '^first_name', '^last_name']
