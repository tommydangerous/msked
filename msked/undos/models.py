from django.db import models
from jobs.models import Job

from locations.models import Location
from msked.utils import pacific_date_time

class Undo(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    job      = models.ForeignKey(Job, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        if self.job:
            u = self.job
        elif self.location:
            u = self.location
        else:
            u = 'Seat Assignment'
        return unicode(u)

    def date_time(self):
        return pacific_date_time(self.created)