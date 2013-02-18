from django.db import models
from django.template.defaultfilters import slugify
from employees.models import Employee

class Location(models.Model):
    created   = models.DateTimeField(auto_now_add=True)
    name      = models.CharField(max_length=30, unique=True)
    occupancy = models.IntegerField(blank=True, null=True)
    slug      = models.SlugField(blank=True, null=True, unique=True)

    def __unicode__(self):
        return unicode(self.name)

    def current_employees(self):
        employees = [e for e in Employee.objects.all() if e.current_location(
            ) and e.current_location().pk == self.pk]
        return sorted(employees, key=lambda e: e.last_name)

    def stations(self):
        return self.station_set.all().order_by('name')

    def save(self, *args, **kwargs):
        self.name = self.name.lower().capitalize()
        self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)