from django.db import models
from employees.models import Employee
from seats.models import Seat

class Assignment(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    seat     = models.ForeignKey(Seat)

    def __unicode__(self):
        return 'Seat %s: %s' % (self.seat, self.employee)

    def date_time(self):
        date = self.created.strftime('%b %d, %y')
        time = self.created.strftime('%I:%M')
        ampm = self.created.strftime('%p').lower()
        return '%s - %s%s' % (date, time, ampm)

    def model(self):
        """Return string of model's class name."""
        return 'assignment'

    def station(self):
        return self.seat.station

    def time(self):
        time  = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return time + am_pm