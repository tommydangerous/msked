from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from employees.models import Employee
from stations.models import Station

class Note(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    content  = models.TextField()
    employee = models.ForeignKey(Employee, blank=True, null=True)
    station  = models.ForeignKey(Station, blank=True, null=True)
    user     = models.ForeignKey(User)
    updated  = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return unicode(self.content)

    def date_time(self):
        date = self.created.strftime('%b %d, %y')
        time = self.created.strftime('%I:%M')
        ampm = self.created.strftime('%p').lower()
        return '%s at %s%s' % (date, time, ampm)

    def model(self):
        return 'note'

    def short(self):
        return self.content[:140]

    def time(self):
        time  = self.created.strftime('%I:%M').lstrip('0')
        am_pm = self.created.strftime('%p').lower()
        return time + am_pm

    def updated_time(self):
        date = self.updated.strftime('%b %d, %y')
        time = self.updated.strftime('%I:%M')
        ampm = self.updated.strftime('%p').lower()
        return '%s at %s%s' % (date, time, ampm)

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Note, self).save(*args, **kwargs)