from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db import connection
from django.db.models import Avg

class EmployeeUltils():
    def get_birthday(date):
        # Get time to start age 
        return (datetime.today()+ relativedelta(years=-date)).date()

class EmployeeQuerySet(models.QuerySet):
    def get_status_active(self):
        """ Get only employees have status is active
        """
        return self.filter(status__gte=1)

    def get_age_avg(self):
        """ Calculate average age of employees
        """
        return self.all().aggregate(Avg('age'))

class EmployeeManager(models.Manager):
    def get_queryset(self):
        return EmployeeQuerySet(self.model, using=self._db)

    def get_age_gt(self):
        return super(EmployeeManager, self).get_queryset().filter(birthday__lt=EmployeeUltils.get_birthday(25))

    def get_status_active(self):
        return self.get_queryset().get_status_active()

    def get_age_avg(self):
        return self.get_queryset().get_age_avg()

    def raw_sql_get_age_gt(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emp_employee WHERE emp_employee.birthday=%s", 25)

        return cursor.fetchall()

    def raw_sql_get_status_active(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emp_employee WHERE emp_employee.status=1")

        return cursor.fetchall()
