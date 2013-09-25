from collections import defaultdict
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from random import shuffle

from jobs.utils import job_check
from tasks.models import Task
from undos.models import Undo
from works.utils import work_check

def change_task_date():
    print ('-' * 10) + ' Change Task Date ' + ('-' * 10)
    for task in Task.objects.all():
        task.created = task.created - timedelta(days=7)
        task.save()

def create_task_for_daily_jobs(jobs, location):
    """Create tasks for the daily jobs that pull from the office."""
    # Excluded employees from the jobs
    ex_pks = []
    for job in jobs:
        ex_pks += [e.pk for e in job.excludes()]
    # Available employees for each job
    avail_dict = defaultdict(list)
    for job in jobs:
        avail = [e for e in location.current_employees(
            ) if job.pk not in e.worked() and e.pk not in ex_pks]
        shuffle(avail)
        avail_dict[job.name] = avail
    for day in range(1, 6):
        # Day 1, 2, 3, 4, 5
        # Employees that worked for the day
        worked = []
        # Mutable list of the jobs
        jobs_list = [job for job in jobs]
        # [After Opening, Wet Copies, After Opening, Wet Copies]; alternate
        job_queue = []
        # after_opening.daily + wet_copies.daily (3 + 3)
        total_needed = sum([job.daily for job in jobs_list])
        for i in range(0, total_needed): # [0, 1, 2, 3, 4, 5]
            job = jobs_list[i % len(jobs_list)] # job_list[0 % 6] = job_list[0]
            job_queue.append(job)
            # If the job appears the same amount as it's daily needed, 
            # remove from the job listing
            if job_queue.count(job) == job.daily:
                jobs_list.remove(job)
        # Assign the jobs by alternating between jobs
        for job in job_queue:
            employees = [e for e in avail_dict[job.name] if e not in worked]
            shuffle(employees)
            employee = employees[0]
            employee.task_set.create(job=job)
            employee.work_set.create(job=job)
            worked.append(employee)
            avail_dict[job.name].remove(employee)
            print '%s Day %s: %s - %s' % (job.name, day, employee, employee.pk)
            print '-' * 20
    for job in jobs:
        Undo.objects.create(job=job)

def create_task_for_weekly_jobs(jobs, location):
    for job in jobs:
        if job.team:
            avail = [e for e in location.current_employees(
                ) if e.team and e.team.pk == job.team.pk and (
                job.pk not in e.worked()) and not e.currently_working()]
        else:
            # Excluded employees from the job
            ex_pks = [e.pk for e in job.excludes()]
            avail = [e for e in location.current_employees(
                ) if job.pk not in e.worked() and not e.currently_working(
                ) and e.pk not in ex_pks]
        shuffle(avail)
        employees = avail[:job.weekly]
        for employee in employees:
            employee.task_set.create(job=job)
            employee.work_set.create(job=job)
        Undo.objects.create(job=job)
        print '%s: %s' % (job, [(e, e.pk) for e in employees])
        print '-' * 20

def set_task(schedule):
    work_check(schedule)
    print ('-' * 10) + ' Set Task ' + ('-' * 10)
    # locations   = schedule.locations_by_occupancy()
    laboratory  = schedule.laboratory()
    office      = schedule.office()
    jobs        = sorted(schedule.jobs(), key=lambda j: j.scarcity())
    daily_jobs  = sorted([job for job in jobs if job.daily], 
        key=lambda x: x.scarcity())
    weekly_jobs = sorted([job for job in jobs if job.weekly],
        key=lambda x: x.scarcity())
    # Create tasks for daily jobs that pull from the office
    # create_task_for_daily_jobs(daily_jobs, locations[1])
    create_task_for_daily_jobs(daily_jobs, office)
    # Create tasks for weekly jobs that pull from the lab
    # create_task_for_weekly_jobs(weekly_jobs, locations[0])
    create_task_for_weekly_jobs(weekly_jobs, laboratory)
    # If in development, change all task dates to a week before
    if settings.DEV:
        change_task_date()

def task_check(schedule, first, second):
    """
    Check to see if there are sufficient employees eligible to work.
    first  = first location employees (always bigger)
    second = second location employees (always smaller)
    """
    jobs = schedule.jobs_by_scarcity()
    print 'First:  %s' % len(first)
    print 'Second: %s' % len(second)
    print ('-' * 10) + ' Task & Job Check ' + ('-' * 10)
    temp = job_check(0, jobs, first, second, first, second)
    if temp:
        return (temp[0], temp[1])
    else:
        return False