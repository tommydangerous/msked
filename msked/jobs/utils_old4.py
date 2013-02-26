from django.core.exceptions import ObjectDoesNotExist
from random import shuffle

def job_check(index, jobs, first, second, f_temp, s_temp, ratio=None):
    job          = jobs[index]
    need         = job.needed()
    avail        = 0
    extra        = 0
    loop_counter = 0
    loop_max     = 50
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
                if new_ratio != ratio:
                    loop_counter = loop_max
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
                    if new_ratio != ratio:
                        loop_counter = loop_max
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
                    if new_ratio != ratio:
                        loop_counter = loop_max
                        break
                else:
                    loop_counter = loop_max
                    break

    elif ratio >= 2:
        while avail < need and loop_counter < loop_max or (
            avail >= len(all_elig) and loop_counter < loop_max) or (
            extra < need and loop_counter < loop_max):

            d = job_loop(index, jobs, first, second, f_temp, s_temp, all_elig, 
                ex_pks, loop_counter, loop_max, need, ratio)
            if d:
                avail        = d['avail']
                extra        = d['extra']
                loop_counter = d['loop_counter']
                new_ratio    = d['new_ratio']
                if new_ratio != ratio:
                    loop_counter = loop_max
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
                if new_ratio != ratio:
                    loop_counter = loop_max
                    break
            else:
                loop_counter = loop_max
                break

    if loop_counter < loop_max:
        # remove eligible employees from the available pool
        e_pks   = [e.pk for e in d['eligible']][:need]
        f_temp  = [e for e in d['f_temp'] if e.pk not in e_pks]
        s_temp  = [e for e in d['s_temp'] if e.pk not in e_pks]
        # remove eligible employees from the extra available pool
        ee_pks  = [e.pk for e in d['ext_elig']][:need]
        ef_temp = [e for e in d['ef_temp'] if e.pk not in ee_pks]
        es_temp = [e for e in d['es_temp'] if e.pk not in ee_pks]
        return (d['new_first'], d['new_second'], f_temp, s_temp, ef_temp, 
            es_temp)
    elif new_ratio and new_ratio != ratio:
        print ('-' * 10) + ' Ratio Change ' + ('-' * 10)
        print job
        print 'Old Ratio: %s, New Ratio: %s' % (ratio, new_ratio)
        print '-' * 20
        temp = job_check(index, jobs, first, second, f_temp, s_temp, new_ratio)
        if temp:
            return temp
        else:
            return False
    else:
        return False

def job_loop(index, jobs, first, second, f_temp, s_temp, all_elig, 
    ex_pks, loop_counter, loop_max, need, ratio):
    job = jobs[index]
    # first job to calculate, last in list
    if index + 1 == len(jobs):
        if job.weekly:
            if len(first) >= len(second):
                shuffle(first)
                new_first = f_temp = ef_temp = first[len(
                    second):] + second
                new_second = s_temp = es_temp = first[:len(second)]
            else:
                shuffle(second)
                new_first = f_temp = ef_temp = second[:len(first)]
                new_second = s_temp = es_temp = second[len(
                    first):] + first
        elif job.daily:
            # employees in lab who have not worked wet copies
            work_emp = [e for e in first if job.pk not in e.worked()]
            shuffle(work_emp)
            # 10 employees in lab who have not worked wet copies
            work_emp = work_emp[:need]
            # 17 employees left over from the lab
            rest_emp = [e for e in first if e not in work_emp]
            shuffle(rest_emp)
            if len(first) >= len(second):
                # # of employees in office - 10
                remaining = len(second) - len(work_emp)
                new_first  = f_temp = ef_temp = (
                    rest_emp[remaining:] + second)
                new_second = s_temp = es_temp = (
                    rest_emp[:remaining] + work_emp)
            else:
                shuffle(second)
                new_first = f_temp = ef_temp = second[:len(first)]
                new_second = s_temp = es_temp = second[len(
                    first):] + first
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
            avail = len(eligible)
            extra = len(ext_elig)
        elif job.daily:
            # the job needs to find avail employees from the lab
            eligible = [e for e in s_temp if job.pk not in e.worked(
                ) and e.pk not in ex_pks]
            ext_elig = [e for e in ef_temp if job.pk not in e.worked(
                ) and e.pk not in ex_pks]
            avail = len(eligible)
            extra = len(ext_elig)
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
        new_ratio = (avail + extra)/float(need)
        d = {
            'avail'       : avail,
            'extra'       : extra,
            'eligible'    : eligible,
            'ext_elig'    : ext_elig,
            'loop_counter': loop_counter + 1,
            'new_first'   : new_first,
            'new_second'  : new_second,
            'new_ratio'   : new_ratio,
            'f_temp'      : f_temp,
            's_temp'      : s_temp,
            'ef_temp'     : ef_temp,
            'es_temp'     : es_temp,
        }
        print '[%s] %s loop: %s' % (index, job, d['loop_counter'])
        print 'Ratio: %s, New Ratio: %s, All Elig: %s' % (ratio, 
            new_ratio, len(all_elig))
        print 'Available: %s, Extra: %s, Need: %s' % (d['avail'], d['extra'], 
            need)
        print '-' * 20
        return d
    else:
        return False