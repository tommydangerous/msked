from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from teams.models import Team

class Employee(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    first_name  = models.CharField(max_length=30)
    floater     = models.BooleanField(default=False)
    last_name   = models.CharField(max_length=30)
    slug        = models.SlugField(blank=True, null=True, unique=True)
    team        = models.ForeignKey(Team, blank=True, null=True)
    tier_lab    = models.IntegerField()
    tier_office = models.IntegerField(blank=True, null=True)
    vacation    = models.BooleanField(default=False)

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def admin_team(self):
        url = reverse('admin:teams_team_change', args=(
            self.team.pk,))
        return '<a href="%s">%s</a>' % (url, self.team)
    admin_team.allow_tags = True
    admin_team.short_description = 'Team'

    def current_job(self):
        if self.currently_working():
            return self.task_set.all().order_by('-created')[0].job

    def current_location(self):
        """Return the most recent location of employee."""
        placement = self.placement_set.all().order_by('-created')
        if placement:
            return placement[0].location

    def current_seat(self):
        """Return current seat if employee is in lab."""
        assignment = self.assignment_set.all().order_by('-created')
        placement = self.placement_set.all().order_by('-created')
        if assignment and placement:
            location = placement[0].location
            seat = assignment[0].seat
            station = seat.station
            if self.current_job() and self.current_job().daily:
                if location.pk != station.location.pk:
                    return seat
            else:
                if location.pk == station.location.pk:
                    return seat

    def currently_working(self):
        task = self.task_set.all().order_by('-created')
        if task:
            task = task[0]
            now = timezone.now()
            day = int(now.strftime('%w'))
            # change for sunday because day = 0
            if task.created > (now - timedelta(days=day)):
                return True

    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def worked(self):
        """Return a list of jobs worked."""
        return [w.job.pk for w in self.work_set.all()]

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower().capitalize()
        self.last_name = self.last_name.lower().capitalize()
        self.slug = slugify('%s %s' % (self.first_name, self.last_name))
        super(Employee, self).save(*args, **kwargs)