from datetime import timedelta
from django.utils import timezone
from random import shuffle
from tasks.models import Task

def task_check(schedule, first, second):
    """
    Check to see if there are sufficient employees eligible to work.
    first  = first location employees (always bigger)
    second = second location employees (always smaller)
    """
    jobs = schedule.jobs_by_scarcity()
    print '-- Task/Job Check --'
    temp = job_check(0, jobs, first, second, first, second)
    if temp:
        return (temp[0], temp[1])
    else:
        return False

def job_check(index, jobs, first, second, f_temp, s_temp):
    job = jobs[index]
    if job.weekly:
        needed = job.weekly
    elif job.daily:
        needed = job.daily * 5
    else:
        needed = 0
    available = 0
    extra = 0
    loop_counter = 0
    loop_max = 100
    if job.team:
        all_eligible = [e for e in job.employees() if job.pk not in e.worked()]
    else:
        all_eligible = [e for e in (first + second) if job.pk not in e.worked()]
    if len(all_eligible)/float(needed) > 3 and job.daily:
        while available < needed and loop_counter < loop_max or (
                available >= len(all_eligible) - needed and loop_counter < loop_max) or (
                extra < needed and loop_counter < loop_max) or (
                extra >= len(all_eligible) - needed and loop_counter < loop_max):
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
        #            employees = require_check(job, first, second)
                    shuffle(first)
        #            first.sort(key=lambda e: job.pk in e.worked())
                    new_first  = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:needed]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = second + rest_emp[remaining:]
                    new_second = s_temp = es_temp = work_emp + rest_emp[:remaining]
            else:
                # loop through job_check again
                temp = job_check(index+1, jobs, first, second, f_temp, s_temp)
                if temp:
                    new_first = temp[0]
                    new_second = temp[1]
                    f_temp = temp[2]
                    s_temp = temp[3]
                    ef_temp = temp[4]
                    es_temp = temp[5]
                else:
                    loop_counter = loop_max
                    break
            if job.weekly:
                if job.team:
                    team = [e.pk for e in job.team.employee_set.all()]
                    eligible = [e for e in f_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                else:
                    eligible = [e for e in f_temp if job.pk not in e.worked()]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked()]
                available = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find available employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                available = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Needed: %s' % (available, extra, needed)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:needed]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:needed]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False
    elif len(all_eligible)/float(needed) > 3:
        while available < needed and loop_counter < loop_max or (
                available >= len(all_eligible) and loop_counter < loop_max) or (
                extra < needed and loop_counter < loop_max) or (
                extra >= len(all_eligible) and loop_counter < loop_max):
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
        #            employees = require_check(job, first, second)
                    shuffle(first)
        #            first.sort(key=lambda e: job.pk in e.worked())
                    new_first  = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:needed]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = second + rest_emp[remaining:]
                    new_second = s_temp = es_temp = work_emp + rest_emp[:remaining]
            else:
                # loop through job_check again
                temp = job_check(index+1, jobs, first, second, f_temp, s_temp)
                if temp:
                    new_first = temp[0]
                    new_second = temp[1]
                    f_temp = temp[2]
                    s_temp = temp[3]
                    ef_temp = temp[4]
                    es_temp = temp[5]
                else:
                    loop_counter = loop_max
                    break
            if job.weekly:
                if job.team:
                    team = [e.pk for e in job.team.employee_set.all()]
                    eligible = [e for e in f_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                else:
                    eligible = [e for e in f_temp if job.pk not in e.worked()]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked()]
                available = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find available employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                available = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Needed: %s' % (available, extra, needed)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:needed]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:needed]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False
    elif len(all_eligible)/float(needed) >= 2 and job.daily:
        while available < needed and loop_counter < loop_max or (
                extra < needed and loop_counter < loop_max) or (
                available >= len(all_eligible) and loop_counter < loop_max):
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
        #            employees = require_check(job, first, second)
                    shuffle(first)
        #            first.sort(key=lambda e: job.pk in e.worked())
                    new_first  = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:needed]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = second + rest_emp[remaining:]
                    new_second = s_temp = es_temp = work_emp + rest_emp[:remaining]
            else:
                # loop through job_check again
                temp = job_check(index+1, jobs, first, second, f_temp, s_temp)
                if temp:
                    new_first = temp[0]
                    new_second = temp[1]
                    f_temp = temp[2]
                    s_temp = temp[3]
                    ef_temp = temp[4]
                    es_temp = temp[5]
                else:
                    loop_counter = loop_max
                    break
            if job.weekly:
                if job.team:
                    team = [e.pk for e in job.team.employee_set.all()]
                    eligible = [e for e in f_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                else:
                    eligible = [e for e in f_temp if job.pk not in e.worked()]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked()]
                available = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find available employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                available = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Needed: %s' % (available, extra, needed)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:needed]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:needed]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False
    elif len(all_eligible)/float(needed) >= 2:
        while available < needed and loop_counter < loop_max or (
                available > len(all_eligible) and loop_counter < loop_max):
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
        #            employees = require_check(job, first, second)
                    shuffle(first)
        #            first.sort(key=lambda e: job.pk in e.worked())
                    new_first  = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:needed]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = second + rest_emp[remaining:]
                    new_second = s_temp = es_temp = work_emp + rest_emp[:remaining]
            else:
                # loop through job_check again
                temp = job_check(index+1, jobs, first, second, f_temp, s_temp)
                if temp:
                    new_first = temp[0]
                    new_second = temp[1]
                    f_temp = temp[2]
                    s_temp = temp[3]
                    ef_temp = temp[4]
                    es_temp = temp[5]
                else:
                    loop_counter = loop_max
                    break
            if job.weekly:
                if job.team:
                    team = [e.pk for e in job.team.employee_set.all()]
                    eligible = [e for e in f_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                else:
                    eligible = [e for e in f_temp if job.pk not in e.worked()]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked()]
                available = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find available employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                available = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Needed: %s' % (available, extra, needed)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:needed]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:needed]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False
    else:
        while available < needed and loop_counter < loop_max:
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
        #            employees = require_check(job, first, second)
                    shuffle(first)
        #            first.sort(key=lambda e: job.pk in e.worked())
                    new_first  = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:needed]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = second + rest_emp[remaining:]
                    new_second = s_temp = es_temp = work_emp + rest_emp[:remaining]
            else:
                # loop through job_check again
                temp = job_check(index+1, jobs, first, second, f_temp, s_temp)
                if temp:
                    new_first = temp[0]
                    new_second = temp[1]
                    f_temp = temp[2]
                    s_temp = temp[3]
                    ef_temp = temp[4]
                    es_temp = temp[5]
                else:
                    loop_counter = loop_max
                    break
            if job.weekly:
                if job.team:
                    team = [e.pk for e in job.team.employee_set.all()]
                    eligible = [e for e in f_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                else:
                    eligible = [e for e in f_temp if job.pk not in e.worked()]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked()]
                available = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find available employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                available = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Needed: %s' % (available, extra, needed)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:needed]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:needed]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False

def set_task(schedule):
    locations = schedule.locations_by_occupancy()
    jobs = sorted(schedule.jobs(), key=lambda j: j.scarcity())
    for job in jobs:
        if job.team:
            available = [e for e in locations[0].current_employees() if (
                e.team and e.team.pk == job.team.pk) and job.pk not in e.worked(
                    ) and not (e.currently_working())]
        else:
            if job.weekly:
                location = locations[0]
            elif job.daily:
                location = locations[1]
            available = [e for e in location.current_employees() if (
                job.pk not in e.worked()) and not e.currently_working()]
        shuffle(available)
        if job.weekly:
            needed = job.weekly
        elif job.daily:
            needed = job.daily * 5
        else:
            needed = 0
        employees = available[:needed]
        for employee in employees:
            employee.task_set.create(job=job)
            employee.work_set.create(job=job)
        print '%s: %s' % (job, employees)
    for task in Task.objects.all():
        task.created = timezone.now() - timedelta(days=30)
        task.save()