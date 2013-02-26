from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from jobs.utils import job_check
from random import shuffle
from tasks.models import Task
from undos.models import Undo
from works.utils import work_check

def change_task_date():
    print ('-' * 10) + ' Change Task Date ' + ('-' * 10)
    for task in Task.objects.all():
        task.created = timezone.now() - timedelta(days=30)
        task.save()
        
def task_check(schedule, first, second):
    """
    Check to see if there are sufficient employees eligible to work.
    first  = first location employees (always bigger)
    second = second location employees (always smaller)
    """
    jobs = schedule.jobs_by_scarcity()
    print ('-' * 10) + ' Task & Job Check ' + ('-' * 10)
    temp = job_check(0, jobs, first, second, first, second)
    if temp:
        return (temp[0], temp[1])
    else:
        return False

def set_task(schedule):
    work_check(schedule)
    print ('-' * 10) + ' Set Task ' + ('-' * 10)
    locations = schedule.locations_by_occupancy()
    jobs = sorted(schedule.jobs(), key=lambda j: j.scarcity())
    for job in jobs:
        if job.team:
            avail = [e for e in locations[0].current_employees(
                ) if e.team and e.team.pk == job.team.pk and (
                job.pk not in e.worked()) and not e.currently_working()]
        else:
            if job.weekly:
                location = locations[0]
            elif job.daily:
                location = locations[1]
            # excluded employees from the job
            ex_pks = [e.pk for e in job.excludes()]
            avail = [e for e in location.current_employees(
                ) if job.pk not in e.worked() and not e.currently_working(
                ) and e.pk not in ex_pks]
        shuffle(avail)
        if job.weekly:
            needed = job.weekly
        elif job.daily:
            needed = job.daily * 5
        else:
            needed = 0
        employees = avail[:needed]
        for employee in employees:
            employee.task_set.create(job=job)
            employee.work_set.create(job=job)
        Undo.objects.create(job=job)
        print '%s: %s' % (job, [e.pk for e in employees])
        print '-' * 20
    if settings.DEV:
        change_task_date()