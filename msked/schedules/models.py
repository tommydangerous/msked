from django.contrib.auth.models import User
from django.db import models
from employees.models import Employee

class Schedule(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=30, unique=True)
    user    = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.name)

    def employees(self):
        employees = Employee.objects.exclude(vacation=True)
        excludes = self.exclude_set.all()
        if excludes:
            for exclude in excludes:
                employees = employees.exclude(team=exclude.team)
        return employees

    def jobs(self):
        return sorted([js.job for js in self.jobschedule_set.all()],
            key=lambda j: j.name)

    def jobs_by_scarcity(self):
        return sorted(self.jobs(), key=lambda j: (j.scarcity(), 
            1.0/j.needed()), reverse=True)

    def locations(self):
        return sorted([ls.location for ls in self.locationschedule_set.all()], 
            key=lambda l: l.name)

    def locations_by_occupancy(self):
        return sorted(self.locations(), key=lambda l: l.occupancy, 
            reverse=True)

    def save(self, *args, **kwargs):
        words = self.name.split(' ')
        name = []
        for word in words:
            name.append(word.lower().capitalize())
        self.name = ' '.join(name)
        super(Schedule, self).save(*args, **kwargs)