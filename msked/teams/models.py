from django.db import models
from locations.models import Location

class Team(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    name     = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name

    def employees(self):
        employees = self.employee_set.order_by('first_name')
        employees = ['%s %s' % (u.first_name, u.last_name)  for u in employees]
        return ', '.join(employees)

    def employees_count(self):
        return self.employee_set.all().count()