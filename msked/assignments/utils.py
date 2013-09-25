from collections import defaultdict
from random import shuffle

from undos.models import Undo
from update_messages.models import UpdateMessage

def assign_seating(schedule):
    laboratory = schedule.laboratory()
    if laboratory:
        employees = list(laboratory.employees_working_here())
        stations  = sorted(list(laboratory.stations()), 
            key=lambda station: station.numerical_name())
        employees_for_job = defaultdict(list)
        seats_with_job    = []
        seats_without_job = []
        # Iterate through each station
        for station in stations:
            # Iterate through each seat
            for seat in station.seats():
                # If the seat has a specific job
                if seat.job:
                    seats_with_job.append(seat)
                    # If value for job name key doesn't exist
                    if not employees_for_job.get(seat.job.name):
                        employees_for_job[seat.job.name] = (
                            seat.job.current_employees())
                else:
                    seats_without_job.append(seat)
        print 'Seats with job:    %s' % len(seats_with_job)
        print 'Seats without job: %s' % len(seats_without_job)
        # Assign seating to specific jobs first
        employees_seated = []
        for seat in seats_with_job:
            employees = employees_for_job.get(seat.job.name)
            if employees:
                employee = employees.pop()
                employee.assignment_set.create(seat=seat)
                employees_seated.append(employee.pk)
        # Assign seating to the rest of the employees without a specific job
        remaining_employees = [e for e in laboratory.current_employees(
            ) if e.pk not in employees_seated]
        shuffle(remaining_employees)
        for seat in seats_without_job:
            if remaining_employees:
                employee = remaining_employees.pop()
                employee.assignment_set.create(seat=seat)
        Undo.objects.create()