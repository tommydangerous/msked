from datetime import timedelta
from django.db import models
from django.utils import timezone

from employees.models import Employee
from teams.models import Team

import itertools

class Job(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    daily   = models.IntegerField(blank=True, null=True)
    name    = models.CharField(max_length=30, unique=True)
    team    = models.ForeignKey(Team, blank=True, null=True)
    weekly  = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)

    def current_employees(self):
        from tasks.models import Task
        need = 0
        if self.daily:
            need = self.daily * 5
        elif self.weekly:
            need = self.weekly
        tasks = Task.objects.filter(job=self).order_by('-created')[:need]
        recent_date = timezone.now()
        within_week = recent_date - timedelta(
            days=int(recent_date.strftime('%w')))
        employees = [t.employee for t in tasks if t.created >= within_week]
        if self.daily:
            return employees
        return sorted(employees, key=lambda e: e.last_name)

    def employees(self):
        return self.team.employee_set.filter(vacation=False)

    def excludes(self):
        ex = self.exclude_set.all()
        teams = [e.team for e in ex]
        emp = [t.employee_set.all() for t in teams]
        emp = list(itertools.chain(*emp))
        return emp

    def model(self):
        """Return a string of the model's class."""
        return 'job'

    def needed(self):
        if self.daily:
            return self.daily * 5
        elif self.weekly:
            return self.weekly
        else:
            return 0

    def scarcity(self):
        """Calculate how scarce eligible workers are for a job."""
        if self.team:
            employees = self.team.employee_set.exclude(vacation=True)
        else:
            from excludes.models import Exclude
            employees = Employee.objects.exclude(vacation=True)
            excludes  = Exclude.objects.filter(job=self)
            if excludes:
                for exclude in excludes:
                    employees = employees.exclude(team=exclude.team)
        employees = len([e for e in employees if self.pk not in e.worked()])
        if self.weekly:
            return float(employees)/self.weekly
        elif self.daily:
            return float(employees)/(self.daily * 5)

    def save(self, *args, **kwargs):
        words = self.name.split(' ')
        name = []
        for word in words:
            name.append(word.lower().capitalize())
        self.name = ' '.join(name)
        super(Job, self).save(*args, **kwargs)