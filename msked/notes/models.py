from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from employees.models import Employee

class Note(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    content  = models.TextField()
    employee = models.ForeignKey(Employee)
    user     = models.ForeignKey(User)
    updated  = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return unicode(self.content)

    def date_time(self):
        date = self.created.strftime('%b %d, %y')
        time = self.created.strftime('%I:%M')
        ampm = self.created.strftime('%p').lower()
        return '%s at %s%s' % (date, time, ampm)

    def short(self):
        return self.content[:140]

    def updated_time(self):
        date = self.updated.strftime('%b %d, %y')
        time = self.updated.strftime('%I:%M')
        ampm = self.updated.strftime('%p').lower()
        return '%s at %s%s' % (date, time, ampm)