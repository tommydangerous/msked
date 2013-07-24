from django.db import models
from jobs.models import Job
from schedules.models import Schedule
from teams.models import Team

class Exclude(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    job      = models.ForeignKey(Job, blank=True, null=True)
    schedule = models.ForeignKey(Schedule, blank=True, null=True)
    team     = models.ForeignKey(Team)

    class Meta:
        unique_together = ('job', 'schedule', 'team',)

    def __unicode__(self):
        return '%s: %s' % (self.team, self.job)