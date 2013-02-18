from django.db import models
from jobs.models import Job
from schedules.models import Schedule

class JobSchedule(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    job      = models.ForeignKey(Job)
    schedule = models.ForeignKey(Schedule)

    class Meta:
        unique_together = ('job', 'schedule')

    def __unicode__(self):
        return unicode(self.job)