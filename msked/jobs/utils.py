from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from random import shuffle

import math

def job_check(index, jobs, first, second, f_temp, s_temp, ratio=None):
    job          = jobs[index]
    need         = job.needed()
    avail        = 0
    extra        = 0
    loop_counter = 0
    loop_max     = settings.LOOP_MAX
    # excluded employees from the job
    ex_pks = [e.pk for e in job.excludes()]
    if job.team:
        emps = job.employees()
    else:
        emps = f_temp + s_temp
    all_elig = [e for e in emps if job.pk not in e.worked(
        ) and e.pk not in ex_pks]
    if not ratio:
        ratio = len(all_elig)/float(need)
    new_ratio = 0
    
    # If the eligible employees is 3 times the amount needed for the week
    # and the job has a daily number and pulls from the office
    if ratio >= 3 and job.daily:
        while avail < need and loop_counter < loop_max or (
            avail >= len(all_elig) - need and loop_counter < loop_max) or (
            extra < need and loop_counter < loop_max) or (
            extra >= len(all_elig) - need and loop_counter < loop_max):

            d = job_loop(index, jobs, first, second, f_temp, s_temp, all_elig, 
                ex_pks, loop_counter, loop_max, need, ratio)
            if d:
                avail        = d['avail']
                extra        = d['extra']
                loop_counter = d['loop_counter']
                new_ratio    = d['new_ratio']
                if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
                    int(new_ratio) - int(ratio)) >= 1:
                    break
            else:
                loop_counter = loop_max
                break

    elif ratio >= 3:
        if index == 0:
            while avail < need and loop_counter < loop_max or (
                avail > len(all_elig) - need and loop_counter < loop_max) or (
                extra > len(all_elig) - need and loop_counter < loop_max):

                d = job_loop(index, jobs, first, second, f_temp, s_temp, 
                    all_elig, ex_pks, loop_counter, loop_max, need, ratio)
                if d:
                    avail        = d['avail']
                    extra        = d['extra']
                    loop_counter = d['loop_counter']
                    new_ratio    = d['new_ratio']
                    if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
                        int(new_ratio) - int(ratio)) >= 1:
                        break
                else:
                    loop_counter = loop_max
                    break

        else:
            while avail < need and loop_counter < loop_max or (
                avail > len(all_elig) - need and loop_counter < loop_max) or (
                extra > len(all_elig) - need and loop_counter < loop_max) or (
                extra < need and loop_counter < loop_max):

                d = job_loop(index, jobs, first, second, f_temp, s_temp, 
                    all_elig, ex_pks, loop_counter, loop_max, need, ratio)
                if d:
                    avail        = d['avail']
                    extra        = d['extra']
                    loop_counter = d['loop_counter']
                    new_ratio    = d['new_ratio']
                    if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
                        int(new_ratio) - int(ratio)) >= 1:
                        break
                else:
                    loop_counter = loop_max
                    break

    elif ratio >= 2:
        if len(first) >= len(second):
            # available needs to be greater than needed
            while avail < need and loop_counter < loop_max or (
                # available cannot be greater than or equal to all eligible
                avail >= len(all_elig) and loop_counter < loop_max) or (
                extra < need and loop_counter < loop_max):
                # not sure what that is for
                # extra < (need - (len(second) - len(first)))):
                d = job_loop(index, jobs, first, second, f_temp, s_temp, 
                    all_elig, ex_pks, loop_counter, loop_max, need, ratio)
                if d:
                    avail        = d['avail']
                    extra        = d['extra']
                    loop_counter = d['loop_counter']
                    new_ratio    = d['new_ratio']
                    if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
                        int(new_ratio) - int(ratio)) >= 1:
                        break
                else:
                    loop_counter = loop_max
                    break
        else:
            if job.daily:
                # Remaining after switch
                ras = len(second) - len(first)
                while (avail < need and loop_counter < loop_max) or (
                    avail >= len(all_elig) and loop_counter < loop_max) or (
                    extra < need - ras and loop_counter < loop_max):

                    d = job_loop(index, jobs, first, second, f_temp, s_temp, 
                        all_elig, ex_pks, loop_counter, loop_max, need, ratio)
                    if d:
                        avail        = d['avail']
                        extra        = d['extra']
                        loop_counter = d['loop_counter']
                        new_ratio    = d['new_ratio']
                        if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
                            int(new_ratio) - int(ratio)) >= 1:
                            break
                    else:
                        loop_counter = loop_max
                        break
            else:
                while avail < need and loop_counter < loop_max or (
                    avail >= len(all_elig) and loop_counter < loop_max) or (
                    extra < need and loop_counter < loop_max):

                    d = job_loop(index, jobs, first, second, f_temp, s_temp, 
                        all_elig, ex_pks, loop_counter, loop_max, need, ratio)
                    if d:
                        avail        = d['avail']
                        extra        = d['extra']
                        loop_counter = d['loop_counter']
                        new_ratio    = d['new_ratio']
                        if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
                            int(new_ratio) - int(ratio)) >= 1:
                            break
                    else:
                        loop_counter = loop_max
                        break

    else:
        while avail < need and loop_counter < loop_max:

            d = job_loop(index, jobs, first, second, f_temp, s_temp, all_elig, 
                ex_pks, loop_counter, loop_max, need, ratio)
            if d:
                avail        = d['avail']
                extra        = d['extra']
                loop_counter = d['loop_counter']
                new_ratio    = d['new_ratio']
                if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
                    int(new_ratio) - int(ratio)) >= 1:
                    break
            else:
                loop_counter = loop_max
                break

    if loop_counter < loop_max:
        if new_ratio >= 1 and new_ratio <= 3 and math.fabs(
            int(new_ratio) - int(ratio)) >= 1:
            print ('-' * 10) + ' Ratio Change ' + ('-' * 10)
            print job
            print 'Old Ratio: %s, New Ratio: %s' % (ratio, new_ratio)
            print '-' * 20
            temp = job_check(index, jobs, first, second, f_temp, s_temp, 
                new_ratio)
            if temp:
                return temp
            else:
                return False
        else:
            # remove eligible employees from the available pool
            # used for calculating employees working in the lab
            # e_pks  = eligible employees
            # f_temp = remaining employees going into the lab
            # s_temp = remaining employees going into the office 
            e_pks   = [e.pk for e in d['eligible']][:need]
            f_temp  = [e for e in d['f_temp'] if e.pk not in e_pks]
            # If the job pulls from the office, don't remove from the pool
            if job.daily:
                s_temp = d.get('s_temp')
            else:
                s_temp  = [e for e in d['s_temp'] if e.pk not in e_pks]

            # remove eligible employees from the extra available pool
            # used for calculating employees working in the office
            # ee_pks  = extra eligible employees
            # ef_temp = extra employees going into the lab
            # es_temp = extra employees going into the office 
            ee_pks  = [e.pk for e in d['ext_elig']][:need]
            ef_temp = d.get('ef_temp')
            es_temp = d.get('es_temp')

            # There is no need to remove from the office pool for daily jobs
            # ef_temp = [e for e in d['ef_temp'] if e.pk not in ee_pks]
            # es_temp = [e for e in d['es_temp'] if e.pk not in ee_pks]
            return (d['new_first'], d['new_second'], f_temp, s_temp, 
                ef_temp, es_temp)

    else:
        return False

def job_loop(index, jobs, first, second, f_temp, s_temp, all_elig, 
    ex_pks, loop_counter, loop_max, need, ratio):
    job = jobs[index]
    # first job to calculate, last in list
    if index == len(jobs) - 1:
        if job.team:
            work_emp_f = [e for e in first if job.pk not in e.worked(
                ) and e in job.employees()]
            work_emp_s = [e for e in second if job.pk not in e.worked(
                ) and e in job.employees()]
            shuffle(work_emp_f)
            shuffle(work_emp_s)
        else:
            work_emp_f = [e for e in first if job.pk not in e.worked()]
            work_emp_s = [e for e in second if job.pk not in e.worked()]
            work_emp_f.sort(key=lambda e: e.team, reverse=True)
            work_emp_s.sort(key=lambda e: e.team, reverse=True)

        if job.weekly:
            if len(first) >= len(second):
                if len(work_emp_s) < need:
                    work_emp = work_emp_f[:need-len(work_emp_s)]
                else:
                    work_emp = []
                rem_emp = [e for e in first if e not in work_emp]
                shuffle(rem_emp)
                new_first  = rem_emp[len(second):] + second + work_emp
                new_second = rem_emp[:len(second)]
            else:
                work_emp = work_emp_s[:need]
                temp_emp = []
                if len(work_emp) < need:
                    temp_emp = work_emp_f[:need-len(work_emp)]
                    work_emp = work_emp + temp_emp
                rem_emp  = [e for e in second if e not in work_emp]
                shuffle(rem_emp)
                new_first  = rem_emp[:len(first)-need] + work_emp
                new_second = rem_emp[len(first)-need:] + first
                if temp_emp:
                    for e in temp_emp:
                        new_second.remove(e)
        # If job needs new employees daily and pulls from the office
        elif job.daily:
            if len(second) >= len(first):
                if len(work_emp_f) < need:
                    work_emp = work_emp_s[:need-len(work_emp_f)]
                else:
                    work_emp = []
                rem_emp = [e for e in second if e not in work_emp]
                shuffle(rem_emp)
                new_first  = rem_emp[:len(first)]
                new_second = rem_emp[len(first):] + first + work_emp
            else:
                work_emp = work_emp_f[:need]
                temp_emp = []
                if len(work_emp) < need:
                    temp_emp = work_emp_s[:need-len(work_emp)]
                    work_emp = work_emp + temp_emp
                rem_emp  = [e for e in first if e not in work_emp]
                shuffle(rem_emp)
                new_first  = rem_emp[len(second)-need:] + second
                new_second = rem_emp[:len(second)-need] + work_emp
                if temp_emp:
                    for e in temp_emp:
                        new_first.remove(e)

        f_temp = ef_temp = new_first
        s_temp = es_temp = new_second

    else:
        # loop through job_check again
        temp = job_check(index+1, jobs, first, second, f_temp, s_temp)
        if temp:
            new_first  = temp[0]
            new_second = temp[1]
            f_temp     = temp[2]
            s_temp     = temp[3]
            ef_temp    = temp[4]
            es_temp    = temp[5]
        else:
            loop_counter = loop_max

    # If loop counter has not reached maximum loops
    if loop_counter < loop_max:
        if job.weekly:
            if job.team:
                team = [e.pk for e in job.team.employee_set.all()]
                eligible = [e for e in f_temp if job.pk not in e.worked(
                    ) and e.pk in team]
                ext_elig = [e for e in es_temp if job.pk not in e.worked(
                    ) and e.pk in team]
            else:
                eligible = [e for e in f_temp if job.pk not in e.worked(
                    ) and e.pk not in ex_pks]
                ext_elig = [e for e in es_temp if job.pk not in e.worked(
                    ) and e.pk not in ex_pks]
        elif job.daily:
            # the job needs to find avail employees from the lab
            eligible = [e for e in s_temp if job.pk not in e.worked(
                ) and e.pk not in ex_pks]
            ext_elig = [e for e in ef_temp if job.pk not in e.worked(
                ) and e.pk not in ex_pks]
        avail = len(eligible)
        extra = len(ext_elig)

        # Fixes something
        if len(all_elig) == need and len(jobs) != (index + 1):
            prev_job = jobs[index + 1]
            if prev_job.weekly:
                prev_need = prev_job.weekly
            if prev_job.daily:
                prev_need = prev_job.daily * 5
            if prev_job.team:
                prev_emp = prev_job.employees()
            else:
                prev_emp = new_first + new_second
            prev_avail = [e for e in prev_emp if prev_job.pk not in e.worked()]
            if len(prev_avail) - prev_need == avail:
                if job.team:
                    all_emp = job.employees()
                else:
                    all_emp = prev_emp
                for employee in all_emp:
                    try:
                        work = employee.work_set.get(job=job)
                        work.delete()
                    except ObjectDoesNotExist:
                        pass

        # If everything works out, return data and continue the job check
        if index < len(jobs) - 1 and loop_counter >= (
            (loop_max/(2 * ((len(jobs) - 1) - index))) - 1):
            if ratio < 2 and avail and avail < need:
                if job.weekly:
                    print ('-' * 10) + ' Extra Elig Extract ' + ('-' * 10)
                    remaining = need - len(eligible)
                    shuffle(ext_elig)
                    # take from extra eligible
                    work_emp = ext_elig[:remaining]
                    shuffle(f_temp)
                    # take some from f_temp
                    switch = f_temp[:remaining]
                    # add from extra eligible to eligible
                    eligible += work_emp
                    # remove work_emp from extra eligible
                    ext_elig = [e for e in ext_elig if e not in eligible]
                    # remove switch from f_temp
                    f_temp = [e for e in f_temp if e not in switch]
                    # add work_emp to f_temp
                    f_temp += work_emp
                    # remove work_emp from s_temp
                    s_temp = [e for e in s_temp if e not in work_emp]
                    # add switch to s_temp
                    s_temp += switch
                    new_first = [e for e in new_first if e not in switch]
                    new_first += work_emp
                    new_second = [e for e in new_second if e not in work_emp]
                    new_second += switch
                    avail = len(eligible)
                    extra = len(ext_elig)
                elif job.daily:
                    pass

        loop_counter += 1
        new_ratio = (avail + extra)/float(need)
        d = {
            'avail'       : avail,
            'extra'       : extra,
            'eligible'    : eligible,
            'ext_elig'    : ext_elig,
            'loop_counter': loop_counter,
            'new_first'   : new_first,
            'new_second'  : new_second,
            'new_ratio'   : new_ratio,
            'f_temp'      : f_temp,
            's_temp'      : s_temp,
            'ef_temp'     : ef_temp,
            'es_temp'     : es_temp,
        }
        print '[%s] %s loop: %s' % (index, job, loop_counter)
        print 'Ratio: %s, New Ratio: %s, All Elig: %s' % (ratio, new_ratio, 
            len(all_elig))
        print 'Available: %s, Extra: %s, Need: %s' % (avail, extra, need)
        print '-' * 20
        return d
    else:
        return False