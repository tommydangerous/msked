from django.db import models
from employees.models import Employee
from jobs.models import Job

class Task(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    job      = models.ForeignKey(Job)

    def __unicode__(self):
        return '%s: %s' % (self.job, self.employee)

    def date_time(self):
        date = self.created.strftime('%b %d, %y')
        time = self.created.strftime('%I:%M')
        ampm = self.created.strftime('%p').lower()
        return '%s - %s%s' % (date, time, ampm)

    def employee_pk(self):
        return self.employee.pk