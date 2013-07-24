from django.db import models
from django.template.defaultfilters import slugify

import itertools

class Location(models.Model):
    created   = models.DateTimeField(auto_now_add=True)
    name      = models.CharField(max_length=30, unique=True)
    occupancy = models.IntegerField(blank=True, null=True)
    slug      = models.SlugField(blank=True, null=True, unique=True)

    def __unicode__(self):
        return unicode(self.name)

    def current_employees(self):
        from employees.models import Employee
        employees = [e for e in Employee.objects.all() if e.current_location(
            ) and e.current_location().pk == self.pk]
        return sorted(employees, key=lambda e: e.last_name)

    def exclusive_employees(self):
        if self.teams():
            emp = [t.employee_set.all() for t in self.teams()]
            emp = list(itertools.chain(*emp))
            return emp
        else:
            return []

    def model(self):
        return 'location'

    def stations(self):
        return self.station_set.all().order_by('name')

    def teams(self):
        return self.team_set.all()

    def save(self, *args, **kwargs):
        self.name = self.name.lower().capitalize()
        self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)