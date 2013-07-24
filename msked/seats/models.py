from django.db import models
from django.utils import timezone
from stations.models import Station

class Seat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=30)
    station = models.ForeignKey(Station)

    class Meta:
        unique_together = ('name', 'station')

    def __unicode__(self):
        return '%s: Seat %s' % (self.station, self.name)

    def assignments(self):
        return self.assignment_set.all()

    def current_employee(self):
        job = self.station.job
        location = self.station.location
        if job and job.daily:
            if self.assignments():
                now = timezone.now()
                day = int(now.strftime('%w'))
                a = self.assignments().order_by('-created')[:(job.needed()/2)]
                a = sorted(list(a), key=lambda am: am.employee.last_name)
                try:
                    e = a[day - 1].employee
                    if e.current_location().pk != location.pk:
                        return e
                except IndexError:
                    pass
        else:
            if self.assignments():
                e = self.assignments().order_by('-created')[0].employee
                if e.current_location():
                    if e.current_location().pk == location.pk:
                        return e

    def model(self):
        return 'seat'

    def number(self):
        try:
            num = int(self.name)
        except ValueError:
            num = None
        return num

    def save(self, *args, **kwargs):
        words = self.name.split(' ')
        name = []
        for word in words:
            name.append(word.lower().capitalize())
        self.name = ' '.join(name)
        super(Seat, self).save(*args, **kwargs)