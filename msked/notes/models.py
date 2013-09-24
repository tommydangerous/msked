from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from msked.utils import pacific_date_time, pacific_time

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
        return pacific_date_time(self.created)

    def model(self):
        return 'note'

    def short(self):
        return self.content[:140]

    def time(self):
        return pacific_time(self.created)

    def updated_time(self):
        return pacific_date_time(self.updated)

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Note, self).save(*args, **kwargs)