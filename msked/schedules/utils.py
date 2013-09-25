from collections import defaultdict
from django.conf import settings
from random import shuffle

from employees.utils import tier_balance
from schedules.models import Schedule
from tasks.utils import change_task_date
from undos.models import Undo
from update_messages.models import UpdateMessage
from works.utils import work_check

def assign_jobs_and_switch_placements(schedule):
    # Check to see if there are enough employees left to work each job
    work_check(schedule)
    all_employees = list(schedule.employees())
    all_jobs      = schedule.jobs()
    daily_jobs = sorted([job for job in all_jobs if job.daily],
        key=lambda job: (job.scarcity(), 1.0/job.needed()))
    weekly_jobs = sorted([job for job in all_jobs if job.weekly],
        key=lambda job: (job.scarcity(), 1.0/job.needed()))
    employees_in = defaultdict(list)
    for location in schedule.locations():
        employees_in[location.name] = []
    # Weekly jobs
    for job in weekly_jobs:
        # If a team works the job
        if job.team:
            pool = [e for e in job.employees() if not e.currently_working(
                ) and job.pk not in e.worked()]
        else:
            # Excluded employees from the job
            ex_pks = [e.pk for e in job.excludes()]
            pool = [e for e in all_employees if not e.currently_working(
                ) and job.pk not in e.worked() and e.pk not in ex_pks]
        # Randomize the pool
        shuffle(pool)
        chosen = pool[:job.needed()]
        for employee in chosen:
            employee.task_set.create(job=job)
            employee.work_set.create(job=job)
            # Remove employee from the all_employees list
            all_employees.remove(employee)
            # Add employee to employees in laboratory
            if employee not in employees_in[schedule.laboratory().name]:
                employees_in[schedule.laboratory().name].append(employee)
        Undo.objects.create(job=job)
        print '%s: %s' % (job, [(e, e.pk) for e in chosen])
        print '-' * 20
    # Daily jobs with employees taken from the office
    # Excluded employees from the job
    exclude_pks = []
    for job in daily_jobs:
        exclude_pks += [e.pk for e in job.excludes()]
    # Available employees for each daily job
    avail_dict = defaultdict(list)
    for job in daily_jobs:
        avail = [e for e in all_employees if job.pk not in e.worked(
            ) and e.pk not in exclude_pks]
        shuffle(avail)
        avail_dict[job.name] = avail
    # For each day Monday through Friday
    for day in range(1, 6):
        # Day 1, 2, 3, 4, 5
        # Employees that worked for the day
        worked = []
        # Mutable list of the jobs
        jobs_list = [job for job in daily_jobs]
        # [After Opening, Wet Copies, After Opening, Wet Copies]; alternate
        job_queue = []
        # after_opening.daily + wet_copies.daily (3 + 3)
        total_needed = sum([job.daily for job in daily_jobs])
        for i in range(0, total_needed): # [0, 1, 2, 3, 4, 5]
            job = jobs_list[i % len(jobs_list)] # job_list[0 % 6] = job_list[0]
            job_queue.append(job)
            # If the job appears the same amount as it's daily needed
            if job_queue.count(job) == job.daily:
                # Remove from the job list
                jobs_list.remove(job)
        # Assign the jobs by alternating between jobs
        for job in job_queue:
            employees = [e for e in avail_dict[job.name] if e not in worked]
            if employees:
                shuffle(employees)
                employee = employees[0]
                employee.task_set.create(job=job)
                employee.work_set.create(job=job)
                # Remove employee from the all_employees list
                if employee in all_employees:
                    all_employees.remove(employee)
                # Add employee employees in office
                if employee not in employees_in[schedule.office().name]:
                    employees_in[schedule.office().name].append(employee)
                worked.append(employee)
                avail_dict[job.name].remove(employee)
                print '%s Day %s: %s - %s' % (job.name, day, 
                    employee, employee.pk)
                print '-' * 20
    for job in daily_jobs:
        Undo.objects.create(job=job)
    # Tier balance
    laboratory   = schedule.laboratory()
    office       = schedule.office()
    lab_needed   = laboratory.occupancy - len(employees_in[laboratory.name])
    remaining    = defaultdict(list)
    balanced     = False
    loop_counter = 0
    while not balanced and loop_counter < settings.LOOP_MAX:
        shuffle(all_employees)
        remaining[laboratory.name] = all_employees[:lab_needed]
        remaining[office.name]     = all_employees[lab_needed:]
        all_lab    = remaining[laboratory.name] + employees_in[laboratory.name]
        all_office = remaining[office.name] + employees_in[office.name]
        balanced   = tier_balance(all_lab, all_office)
        loop_counter +=1
        print loop_counter
    # Assign placements to locations
    for location in schedule.locations():
        for employee in employees_in[location.name] + remaining[location.name]:
            employee.placement_set.create(location=location)
        Undo.objects.create(location=location)

    if settings.DEV:
        # CHANGE TASK DATE FOR TESTING PURPOSES ONLY
        change_task_date()

# for location in sorted(schedule.locations(), key=lambda l: l.occupancy):
#     for employee in employees_in[location.name]:
#         employee.placement_set.create(location=location)
#     # 25 - 10 = 15
#     remaining_number = location.occupancy - len(employees_in[location.name])
#     for employee in all_employees[:remaining_number]:
#         employee.placement_set.create(location=location)
#         if employee in all_employees:
#             all_employees.remove(employee)
#     Undo.objects.create(location=location)