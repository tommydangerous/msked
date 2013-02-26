from django.core.exceptions import ObjectDoesNotExist
from random import shuffle

def job_check(index, jobs, first, second, f_temp, s_temp):
    job = jobs[index]
    if job.weekly:
        need = job.weekly
    elif job.daily:
        need = job.daily * 5
    else:
        need = 0
    avail = 0
    extra = 0
    loop_counter = 0
    loop_max = 100
    if job.team:
        all_elig = [e for e in job.employees() if job.pk not in e.worked()]
    else:
        all_elig = [e for e in (first + second) if job.pk not in e.worked()]
    if len(all_elig)/float(need) >= 3 and job.daily:
        while avail < need and loop_counter < loop_max or (
            avail >= len(all_elig) - need and loop_counter < loop_max) or (
            extra < need and loop_counter < loop_max) or (
            extra >= len(all_elig) - need and loop_counter < loop_max):
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
                    shuffle(first)
                    new_first = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:need]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = (
                        second + rest_emp[remaining:])
                    new_second = s_temp = es_temp = (
                        work_emp + rest_emp[:remaining])
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
                avail = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find avail employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                avail = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Need: %s' % (avail, extra, need)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:need]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:need]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False
    elif len(all_elig)/float(need) >= 3:
        if index == 0:
            while avail < need and loop_counter < loop_max or (
                avail > len(all_elig) - need and loop_counter < loop_max) or (
                extra > len(all_elig) - need and loop_counter < loop_max):
                # first job to calculate, last in list
                if index + 1 == len(jobs):
                    if job.weekly:
                        shuffle(first)
                        new_first = f_temp = ef_temp = first[len(second):] + second
                        new_second = s_temp = es_temp = first[:len(second)]
                    elif job.daily:
                        work_emp = [e for e in first if job.pk not in e.worked()]
                        shuffle(work_emp)
                        work_emp = work_emp[:need]
                        rest_emp = [e for e in first if e not in work_emp]
                        shuffle(rest_emp)
                        remaining = len(second) - len(work_emp)
                        new_first  = f_temp = ef_temp = (
                            second + rest_emp[remaining:])
                        new_second = s_temp = es_temp = (
                            work_emp + rest_emp[:remaining])
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
                    avail = len(eligible)
                    extra = len(ext_elig)
                elif job.daily:
                    # the job needs to find avail employees from the lab
                    eligible = [e for e in s_temp if job.pk not in e.worked()]
                    avail = len(eligible)
                    ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                    extra = len(ext_elig)
                else:
                    loop_counter = loop_max
                    print 'Job has no required amount'
                    break
                loop_counter += 1
                print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
                print 'Available: %s, Extra: %s, Need: %s' % (avail, extra, need)
            if loop_counter < loop_max:
                # remove eligible employees from pool of potential workers
                e_pks = [e.pk for e in eligible][:need]
                f_temp = [e for e in f_temp if e.pk not in e_pks]
                s_temp = [e for e in s_temp if e.pk not in e_pks]
                ee_pks = [e.pk for e in ext_elig][:need]
                ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
                es_temp = [e for e in es_temp if e.pk not in ee_pks]
                return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
            else:
                return False
        else:
            while avail < need and loop_counter < loop_max or (
                avail > len(all_elig) - need and loop_counter < loop_max) or (
                extra < need and loop_counter < loop_max) or (
                extra > len(all_elig) - need and loop_counter < loop_max):
                # first job to calculate, last in list
                if index + 1 == len(jobs):
                    if job.weekly:
                        shuffle(first)
                        new_first = f_temp = ef_temp = first[len(second):] + second
                        new_second = s_temp = es_temp = first[:len(second)]
                    elif job.daily:
                        work_emp = [e for e in first if job.pk not in e.worked()]
                        shuffle(work_emp)
                        work_emp = work_emp[:need]
                        rest_emp = [e for e in first if e not in work_emp]
                        shuffle(rest_emp)
                        remaining = len(second) - len(work_emp)
                        new_first  = f_temp = ef_temp = (
                            second + rest_emp[remaining:])
                        new_second = s_temp = es_temp = (
                            work_emp + rest_emp[:remaining])
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
                    avail = len(eligible)
                    extra = len(ext_elig)
                elif job.daily:
                    # the job needs to find avail employees from the lab
                    eligible = [e for e in s_temp if job.pk not in e.worked()]
                    avail = len(eligible)
                    ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                    extra = len(ext_elig)
                else:
                    loop_counter = loop_max
                    print 'Job has no required amount'
                    break
                loop_counter += 1
                print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
                print 'Available: %s, Extra: %s, Need: %s' % (avail, extra, need)
            if loop_counter < loop_max:
                # remove eligible employees from pool of potential workers
                e_pks = [e.pk for e in eligible][:need]
                f_temp = [e for e in f_temp if e.pk not in e_pks]
                s_temp = [e for e in s_temp if e.pk not in e_pks]
                ee_pks = [e.pk for e in ext_elig][:need]
                ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
                es_temp = [e for e in es_temp if e.pk not in ee_pks]
                return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
            else:
                return False
    elif len(all_elig)/float(need) >= 2 and job.daily:
        while avail < need and loop_counter < loop_max or (
                extra < need and loop_counter < loop_max) or (
                avail >= len(all_elig) and loop_counter < loop_max):
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
                    shuffle(first)
                    new_first = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:need]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = (
                        second + rest_emp[remaining:])
                    new_second = s_temp = es_temp = (
                        work_emp + rest_emp[:remaining])
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
                avail = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find avail employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                avail = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Need: %s' % (avail, extra, need)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:need]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:need]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False
    elif len(all_elig)/float(need) >= 2:
        while avail < need and loop_counter < loop_max or (
                avail > len(all_elig) and loop_counter < loop_max):
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
                    shuffle(first)
                    new_first = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:need]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = (
                        second + rest_emp[remaining:])
                    new_second = s_temp = es_temp = (
                        work_emp + rest_emp[:remaining])
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
                avail = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find avail employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                avail = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Need: %s' % (avail, extra, need)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:need]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:need]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False
    else:
        while avail < need and loop_counter < loop_max:
            # first job to calculate, last in list
            if index + 1 == len(jobs):
                if job.weekly:
                    shuffle(first)
                    new_first = f_temp = ef_temp = first[len(second):] + second
                    new_second = s_temp = es_temp = first[:len(second)]
                elif job.daily:
                    work_emp = [e for e in first if job.pk not in e.worked()]
                    shuffle(work_emp)
                    work_emp = work_emp[:need]
                    rest_emp = [e for e in first if e not in work_emp]
                    shuffle(rest_emp)
                    remaining = len(second) - len(work_emp)
                    new_first  = f_temp = ef_temp = (
                        second + rest_emp[remaining:])
                    new_second = s_temp = es_temp = (
                        work_emp + rest_emp[:remaining])
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
                    team = [e.pk for e in job.employees()]
                    eligible = [e for e in f_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked(
                        ) and e.pk in team]
                else:
                    eligible = [e for e in f_temp if job.pk not in e.worked()]
                    ext_elig = [e for e in es_temp if job.pk not in e.worked()]
                avail = len(eligible)
                extra = len(ext_elig)
            elif job.daily:
                # the job needs to find avail employees from the lab
                eligible = [e for e in s_temp if job.pk not in e.worked()]
                avail = len(eligible)
                ext_elig = [e for e in ef_temp if job.pk not in e.worked()]
                extra = len(ext_elig)
            else:
                loop_counter = loop_max
                print 'Job has no required amount'
                break
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
            loop_counter += 1
            print 'Job[%s] %s loop: %s' % (index, job, loop_counter)
            print 'Available: %s, Extra: %s, Need: %s' % (avail, extra, need)
        if loop_counter < loop_max:
            # remove eligible employees from pool of potential workers
            e_pks = [e.pk for e in eligible][:need]
            f_temp = [e for e in f_temp if e.pk not in e_pks]
            s_temp = [e for e in s_temp if e.pk not in e_pks]
            ee_pks = [e.pk for e in ext_elig][:need]
            ef_temp = [e for e in ef_temp if e.pk not in ee_pks]
            es_temp = [e for e in es_temp if e.pk not in ee_pks]
            return (new_first, new_second, f_temp, s_temp, ef_temp, es_temp)
        else:
            return False