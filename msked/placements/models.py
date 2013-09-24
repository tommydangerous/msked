from django.core.urlresolvers import reverse
from django.db import models
from employees.models import Employee
from locations.models import Location
from msked.utils import pacific_date_time, pacific_time

class Placement(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return '%s: %s' % (self.location, self.employee)

    def admin_employee(self):
        url = reverse('admin:employees_employee_change', 
            args=(self.employee.pk,))
        return '<a href="%s">%s</a>' % (url, self.employee.name())
    admin_employee.allow_tags = True
    admin_employee.short_description = 'Employee'

    def admin_location(self):
        url = reverse('admin:locations_location_change', 
            args=(self.location.pk,))
        return '<a href="%s">%s</a>' % (url, self.location)
    admin_location.allow_tags = True
    admin_location.short_description = 'Location'

    def date_time(self):
        return pacific_date_time(self.created)
        
    def model(self):
        """Return string of model's class name."""
        return 'placement'

    def team(self):
        return self.employee.team

    def time(self):
        return pacific_time(self.created)