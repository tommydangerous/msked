from collections import defaultdict
from django.conf import settings
from django.db.models import Q
from employees.models import Employee
from employees.utils import tier_lab_sum, tier_balance
from random import shuffle
from tasks.utils import task_check
from undos.models import Undo
from works.utils import work_check

def set_placements(schedule):
    employees = list(schedule.employees())
    # work locations for this schedule
    locations = sorted(schedule.locations(), 
        key=lambda l: l.occupancy, reverse=True)
    # create dictionary with empty list for each location
    location_dict = defaultdict(list)
    for location in locations:
        location_dict[location] = []
    # if schedule has at least 1 location with an occupancy number
    if locations and locations[0].occupancy:
        first_loc  = locations[0]
        second_loc = locations[1]
        # separate location exclusive employees
        exl_emp = first_loc.exclusive_employees()
        exl_pks = [e.pk for e in exl_emp]
        employees = [e for e in employees if e.pk not in exl_pks]
        balanced     = False
        loop_counter = 0
        loop_max     = settings.LOOP_MAX
        work_check(schedule)
        # keep shuffling until the tier levels are balanced in all locations
        # or until the script has looped over itself 1000 times
        while not location_dict[first_loc] and not balanced and (
            loop_counter < loop_max):
            shuffle(employees)
            needed = first_loc.occupancy - len(exl_emp)
            first_emp  = employees[:needed]
            second_emp = employees[needed:]
            temp = task_check(schedule, first_emp, second_emp)
            if temp:
                location_dict[first_loc]  = temp[0] + exl_emp
                location_dict[second_loc] = temp[1]
                balanced = tier_balance(temp[0], temp[1])
            else:
                loop_counter = loop_max
                break
            loop_counter += 1
            print 'Set placement loop counter: %s' % loop_counter
        if loop_counter < loop_max:
            for location in locations:
                for employee in location_dict[location]:
                    # create employee placements for location
                    employee.placement_set.create(location=location)
                Undo.objects.create(location=location)
            return loop_counter
        else:
            return False

def switch_placements(schedule):
    all_employees = Employee.objects.exclude(vacation=True)
    excludes = schedule.exclude_set.all()
    if excludes:
        # exclude employees on certain teams
        for exclude in excludes:
            all_employees = all_employees.exclude(team=exclude.team)
    all_employees = list(all_employees)
    # work locations for this schedule
    # if office has an occupancy, 
    # office becomes the first location when reversed
    # ---------- NOT GOOD ----------
    # locations = sorted(schedule.locations(), 
    #     key=lambda l: l.occupancy, reverse=True)
    # Laboratory must be first, Office must be second
    locations = sorted(schedule.locations(), key=lambda l: l.occupancy)
    if len(locations) >= 2:
        # check to see if employees are placed at both locations
        first_loc  = locations[0]
        second_loc = locations[1]
        if not first_loc.current_employees() and not (
                second_loc.current_employees()):
            return set_placements(schedule)
        else:
            # create dictionary with empty list for each location
            location_dict = defaultdict(list)
            # previous location dictionary
            prev_dict = defaultdict(list)
            for location in locations:
                location_dict[location] = []
                # store the location's previous employees
                prev_dict[location] = (
                    [e for e in location.current_employees() if not (
                        e.vacation)])
            employees = prev_dict[first_loc] + prev_dict[second_loc]
            # check to see if any employees came back from vacation
            new_extra = [e for e in all_employees if e not in employees]
            for employee in new_extra:
                if employee.current_location():
                    # place them at their last worked location
                    prev_dict[employee.current_location].append(employee)
                else:
                    # place them in the second location
                    prev_dict[second_loc].append(employee)
            if first_loc.occupancy:
                balanced     = False
                loop_counter = 0
                loop_max     = settings.LOOP_MAX
                # check to see if there are enough employees left to
                # work at each job for the week
                work_check(schedule)
                # separate location exclusive employees
                exl_emp  = first_loc.exclusive_employees()
                exl_pks  = [e.pk for e in exl_emp]
                while not location_dict[first_loc] and not balanced and (
                    loop_counter < loop_max):
                    prev_femp = prev_dict[first_loc]
                    prev_femp = [e for e in prev_femp if e.pk not in exl_pks]
                    prev_semp = prev_dict[second_loc]
                    temp = task_check(schedule, prev_femp, prev_semp)
                    if temp:
                        location_dict[first_loc]  = temp[0] + exl_emp
                        location_dict[second_loc] = temp[1]
                        balanced = tier_balance(temp[0], temp[1])
                    else:
                        loop_counter = loop_max
                        break
                    loop_counter += 1
                    print 'Switch placement loop counter: %s' % loop_counter
                if loop_counter < loop_max:
                    for location in locations:
                        for employee in location_dict[location]:
                            # create employee placements for location
                            employee.placement_set.create(location=location)
                        Undo.objects.create(location=location)
                    return loop_counter
                else:
                    return False