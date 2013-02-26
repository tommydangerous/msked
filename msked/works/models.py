from django.db import models
from employees.models import Employee
from jobs.models import Job

# shows what employee has worked what job in the current cycle
class Work(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    job      = models.ForeignKey(Job)

    class Meta:
        unique_together = ('employee', 'job')

    def __unicode__(self):
        return '%s: %s' % (self.job, self.employee)

    def current_location(self):
        return self.employee.current_location()