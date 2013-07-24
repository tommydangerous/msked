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

    def model(self):
        """Return string of model's class name."""
        return 'task'

    def time(self):
        time  = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return time + am_pm