# import datetime

from django.db import models

from department.models import Department
from emp.managers import EmployeeManager

# Define model Employee
class Employee(models.Model):
    """ Model Employee
    """

    STATUS_CHOICES = (
        (0, 'inactive'),
        (1, 'active'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birthday = models.DateField()
    email = models.EmailField(max_length=254)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    objects = EmployeeManager()

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])
