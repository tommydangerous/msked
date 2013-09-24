from django.db import models
from employees.models import Employee
from msked.utils import pacific_date_time, pacific_time
from seats.models import Seat

class Assignment(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    seat     = models.ForeignKey(Seat)

    def __unicode__(self):
        return 'Seat %s: %s' % (self.seat, self.employee)

    def date_time(self):
        return pacific_date_time(self.created)

    def model(self):
        """Return string of model's class name."""
        return 'assignment'

    def station(self):
        return self.seat.station

    def time(self):
        return pacific_time(self.created)