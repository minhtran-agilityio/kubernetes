from django.db import models

# Define model Department
class Department(models.Model):
    """ Model Department
    """

    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name
