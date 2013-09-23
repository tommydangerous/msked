from collections import defaultdict
from random import shuffle
from undos.models import Undo

def assign_seating(schedule):
    # locations = schedule.locations_by_occupancy()
    # if locations:
    # location = locations[0]
    location_schedule = schedule.locationschedule_set.filter(
        location__name__icontains='lab')
    if location_schedule:
        location = location_schedule[0].location
        job_seats = defaultdict(list)
        for station in location.stations():
            if station.job:
                job_seats[station.job] = station.job.current_employees()
        employees = [e for e in location.current_employees(
            ) if not e.currently_working()]
        shuffle(employees)
        for station in location.stations():
            # wet copies
            if station.job and station.job.daily:
                e = job_seats[station.job]
                seats = station.seats()
                seat_one = range(0, len(e), 2)
                seat_two = range(1, len(e), 2)
                for n in seat_one:
                    e[n].assignment_set.create(seat=seats[0])
                for n in seat_two:
                    e[n].assignment_set.create(seat=seats[1])
            else:
                for seat in station.seats():
                    # Sarah
                    if station.number() == 2 and seat.number() in (2, 4):
                        pass
                    # wet entry
                    elif station.number() == 6 and seat.number() in (2, 4):
                        if station.job and job_seats[station.job]:
                            employee = job_seats[station.job].pop()
                            if employee.current_location().pk == location.pk:
                                employee.assignment_set.create(seat=seat)
                    # after opening
                    elif station.number() == 7 and seat.number() == 1:
                        if station.job and job_seats[station.job]:
                            employee = job_seats[station.job].pop()
                            if employee.current_location().pk == location.pk:
                                employee.assignment_set.create(seat=seat)
                    # after opening
                    elif station.number() == 8 and seat.number() in (2, 4):
                        if station.job and job_seats[station.job]:
                            employee = job_seats[station.job].pop()
                            if employee.current_location().pk == location.pk:
                                employee.assignment_set.create(seat=seat)
                    # rejects
                    elif station.name == 'Rejects':
                        if station.job and job_seats[station.job]:
                            employee = job_seats[station.job].pop()
                            if employee.current_location().pk == location.pk:
                                employee.assignment_set.create(seat=seat)
                    # everybody else
                    elif employees:
                        employee = employees.pop()
                        employee.assignment_set.create(seat=seat)
        Undo.objects.create()