from django.db import models
from employees.models import Employee
from teams.models import Team

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
        if self.daily:
            need = self.daily * 5
        elif self.weekly:
            need = self.weekly
        else:
            need = 0
        tasks = Task.objects.filter(job=self).order_by('-created')[:need]
        employees = [t.employee for t in tasks]
        return sorted(employees, key=lambda e: e.last_name)

    def employees(self):
        return self.team.employee_set.filter(vacation=False)

    def needed(self):
        if self.daily:
            return self.daily * 5
        elif self.weekly:
            return self.weekly

    def scarcity(self):
        """Calculate how scarce eligible workers are for a job."""
        if self.team:
            employees = self.team.employee_set.exclude(vacation=True)
        else:
            from excludes.models import Exclude
            employees = Employee.objects.exclude(vacation=True)
            excludes = Exclude.objects.filter(job=None)
            if excludes:
                for exclude in excludes:
                    employees = employees.exclude(team=exclude.team)
            employees = employees
        employees = len([e for e in employees if self.pk not in e.worked()])
        if self.weekly:
            return employees/self.weekly
        elif self.daily:
            return employees/(self.daily * 5)

    def scarcity_old(self):
        """Calculate how scarce eligible workers are for a job."""
        if self.team:
            employees = self.team.employee_set.exclude(vacation=True).count()
        else:
            from excludes.models import Exclude
            employees = Employee.objects.exclude(vacation=True)
            excludes = Exclude.objects.filter(job=None)
            if excludes:
                for exclude in excludes:
                    employees = employees.exclude(team=exclude.team)
            employees = employees.count()
        if self.weekly:
            return employees/float(self.weekly)
        elif self.daily:
            return employees/float(self.daily * 5)

    def save(self, *args, **kwargs):
        words = self.name.split(' ')
        name = []
        for word in words:
            name.append(word.lower().capitalize())
        self.name = ' '.join(name)
        super(Job, self).save(*args, **kwargs)