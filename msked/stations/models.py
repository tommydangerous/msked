from django.db import models
from jobs.models import Job
from locations.models import Location

class Station(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    job      = models.ForeignKey(Job, blank=True, null=True)
    location = models.ForeignKey(Location)
    name     = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return 'Station %s' % self.name

    def number(self):
        try:
            num = int(self.name)
        except ValueError:
            num = None
        return num

    def seats(self):
        return self.seat_set.all().order_by('name')

    def save(self, *args, **kwargs):
        words = self.name.split(' ')
        name = []
        for word in words:
            name.append(word.lower().capitalize())
        self.name = ' '.join(name)
        super(Station, self).save(*args, **kwargs)