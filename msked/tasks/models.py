from django.db import models
from employees.models import Employee
from jobs.models import Job
from msked.utils import pacific_date_time, pacific_time

class Task(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    job      = models.ForeignKey(Job)

    def __unicode__(self):
        return '%s: %s' % (self.job, self.employee)

    def date_time(self):
        return pacific_date_time(self.created)
        
    def employee_pk(self):
        return self.employee.pk

    def model(self):
        """Return string of model's class name."""
        return 'task'

    def time(self):
        return pacific_time(self.created)