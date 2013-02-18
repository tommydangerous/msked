from django.db import models
from locations.models import Location
from schedules.models import Schedule

class LocationSchedule(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location)
    schedule = models.ForeignKey(Schedule)

    class Meta:
        unique_together = ('location', 'schedule')

    def __unicode__(self):
        return unicode(self.location)