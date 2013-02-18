from collections import defaultdict
from django.db.models import Q
from employees.models import Employee
from employees.utils import tier_lab_sum, tier_lab_balance_check
from random import shuffle
from tasks.utils import task_check
from undos.models import Undo
from works.utils import work_check

def set_placements(schedule):
    employees = list(schedule.employees())
    # the tier lab sum of all employees
    total_tier = sum([e.tier_lab for e in employees])
    # work locations for this schedule
    locations = sorted(schedule.locations(), 
        key=lambda l: l.occupancy, reverse=True)
    # create dictionary with empty list for each location
    location_dict = defaultdict(list)
    for location in locations:
        location_dict[location] = []
    # if schedule has at least 1 location with an occupancy number
    if locations and locations[0].occupancy:
        # minimum tier level required for first work location
        min_tier = locations[0].occupancy/float(len(employees)) * total_tier
        loop_counter = 0
        loop_max = 1000
        # keep shuffling until the tier levels are balanced in all locations
        # or until the script has looped over itself 10,000 times
        while not location_dict[locations[0]] or not tier_lab_balance_check(
                location_dict[locations[0]], 
                    min_tier) and loop_counter < loop_max:
            shuffle(employees)
            temp = task_check(schedule, employees[:locations[0].occupancy], 
                employees[locations[0].occupancy:])
            if temp:
                location_dict[locations[0]] = temp[0]
                location_dict[locations[1]] = temp[1]
            else:
                loop_counter = loop_max
                break
            loop_counter += 1
        if loop_counter < loop_max:
            for location in locations:
                for employee in location_dict[location]:
                    # create employee placements for location
                    employee.placement_set.create(location=location)
                Undo.objects.create(location=location)
        print 'Loop counter: %s' % loop_counter
        return loop_counter

def switch_placements(schedule):
    all_employees = Employee.objects.exclude(vacation=True)
    excludes = schedule.exclude_set.all()
    if excludes:
        # exclude employees on certain teams
        for exclude in excludes:
            all_employees = all_employees.exclude(team=exclude.team)
    all_employees = list(all_employees)
    # work locations for this schedule
    locations = sorted(schedule.locations(), 
        key=lambda l: l.occupancy, reverse=True)
    if len(locations) >= 2:
        # check to see if employees are placed at both locations
        if not locations[0].current_employees() and not (
                locations[1].current_employees()):
            set_placements(schedule)
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
            employees = prev_dict[locations[0]] + prev_dict[locations[1]]
            # check to see if any employees came back from vacation
            new_extra = [e for e in all_employees if e not in employees]
            # the tier lab sum of all employees
            total_tier = sum([e.tier_lab for e in employees])
            for employee in new_extra:
                if employee.current_location():
                    # place them at their last worked location
                    prev_dict[employee.current_location].append(employee)
                else:
                    # place them in the second location
                    prev_dict[locations[1]].append(employee)
            if locations[0].occupancy:
                # minimum tier level required for first work location
                min_tier = locations[0].occupancy/float(len(
                    employees)) * total_tier
                loop_counter = 0
                loop_max = 1000
                # check to see if there are enough employees left to
                # work at each job for the week
                work_check(schedule)
                while not location_dict[locations[0]] or not (
                    tier_lab_balance_check(location_dict[locations[0]], 
                        min_tier)) and loop_counter < loop_max:
                    # if first location employees are 
                    # less than second location employees
                    if locations[0].occupancy < len(prev_dict[locations[1]]):
                        temp = task_check(schedule, prev_dict[locations[1]], 
                            prev_dict[locations[0]])
                        if temp:
                            location_dict[locations[0]] = temp[1]
                            location_dict[locations[1]] = temp[0]
                        else:
                            loop_counter = loop_max
                            break
                    else:
                        temp = task_check(schedule, prev_dict[locations[0]], 
                            prev_dict[locations[1]])
                        if temp:
                            location_dict[locations[0]] = temp[0]
                            location_dict[locations[1]] = temp[1]
                        else:
                            loop_counter = loop_max
                            break
                    loop_counter += 1
                if loop_counter < loop_max:
                    for location in locations:
                        for employee in location_dict[location]:
                            # create employee placements for location
                            employee.placement_set.create(location=location)
                        Undo.objects.create(location=location)
                print 'Switch placement loop counter: %s' % loop_counter
                return loop_counter