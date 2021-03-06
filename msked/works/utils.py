from django.core.exceptions import ObjectDoesNotExist

def work_check(schedule):
    """
    Check to see if there are enough employees 
    left to work at each job for the week.
    """
    jobs = schedule.jobs_by_scarcity()
    print ('-' * 10) + ' Work Check ' + ('-' * 10)
    for job in jobs:
        if job.team:
            eligible = job.employees()
        else:
            eligible = schedule.employees()
        if job.daily:
            needed = job.daily * 5
        elif job.weekly:
            needed = job.weekly
        # excluded employees from the job
        ex_pks = [e.pk for e in job.excludes()]
        available = [e for e in eligible if job.pk not in e.worked(
            ) and e.pk not in ex_pks]
        print '%s, Available: %s' % (job, len(available))
        if len(available) < needed:
#            for employee in available:
                # create require for employees who have not worked
#                employee.require_set.create(job=job)
            for employee in eligible:
                try:
                    work = employee.work_set.get(job=job)
                    # reset employee work cycle by deleting work record
                    work.delete()
                except ObjectDoesNotExist:
                    pass
            print '%s work cleared' % job