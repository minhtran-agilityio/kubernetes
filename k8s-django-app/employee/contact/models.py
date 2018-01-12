from django.db import models
from emp.models import Employee

# Model Contact
class Contact(models.Model):
    """ Model Contact
    """

    name = models.CharField(max_length=60)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
