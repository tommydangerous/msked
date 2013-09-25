from collections import defaultdict
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, RequestContext

from assignments.utils import assign_seating
from placements.utils import set_placements, switch_placements
from schedules.models import Schedule
from schedules.utils import assign_jobs_and_switch_placements
from tasks.utils import set_task

import django_rq
import json

@login_required
def assign_and_switch(request, pk):
    """Assign jobs then create placements"""
    schedule = get_object_or_404(Schedule, pk=pk)
    assign_jobs_and_switch_placements(schedule)
    messages.success(request, 'Jobs assigned, places switched')
    return HttpResponseRedirect(reverse('schedules.views.detail', 
        args=[schedule.pk]))

@login_required
def assignment(request, pk):
    """Create assignment for station seating for employees."""
    schedule = get_object_or_404(Schedule, pk=pk)
    assign_seating(schedule)
    messages.success(request, 'Seats have been assigned')
    return HttpResponseRedirect(reverse('root_path'))

def detail(request, pk):
    """Schedule detail page."""
    schedule    = get_object_or_404(Schedule, pk=pk)
    d = {
        'jobs_url': reverse('schedules.views.jobs',
            args=[schedule.pk]),
        'locations_url': reverse('schedules.views.locations', 
            args=[schedule.pk]),
        'schedule' : schedule,
        'title'    : schedule.name,
    }
    return render_to_response('schedules/detail.html', d, 
        context_instance=RequestContext(request))

def jobs(request, pk):
    """Return ajax jobs for schedule."""
    schedule    = get_object_or_404(Schedule, pk=pk)
    all_jobs    = schedule.jobs()
    daily_jobs  = [job for job in all_jobs if job.daily]
    weekly_jobs = [job for job in all_jobs if job.weekly]
    d = {
        'daily_jobs' : daily_jobs,
        'weekly_jobs': weekly_jobs,
    }
    jobs = loader.get_template('schedules/jobs.html')
    context = RequestContext(request, d)
    data = {
        'jobs': jobs.render(context),
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')

def locations(request, pk):
    """Return ajax locations for schedule."""
    schedule = get_object_or_404(Schedule, pk=pk)
    # [(location, employees), (location, employees)]
    groups = [(l, l.employees_working_here()) for l in schedule.locations()]
    d = {
        'locations': groups,
    }
    locations = loader.get_template('schedules/locations.html')
    context   = RequestContext(request, d)
    data = {
        'locations': locations.render(context),
    }
    return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def placement(request, pk):
    """Create placement and set/switch locations for employees."""
    schedule = get_object_or_404(Schedule, pk=pk)
    if settings.DEV:
        if switch_placements(schedule):
            messages.success(request, 'Placements switched')
        else:
            messages.error(request, 'Nothing was done, loop exceeded maximum')
    else:
        # Place in queue to run in the background
        django_rq.enqueue(switch_placements, schedule)
        messages.success(request, 'Switching placements, please wait')
    return HttpResponseRedirect(reverse('schedules.views.detail', 
        args=[schedule.pk]))

def root(request):
    schedule = Schedule.objects.all().order_by('created')[0]
    location_schedule = schedule.locationschedule_set.filter(
        location__name__icontains='lab')
    d = {}
    if location_schedule:
        location = location_schedule[0].location
        stations = sorted(list(location.stations()), 
            key=lambda station: station.numerical_name())
        max_stations_per_side = 7
        if len(stations) > max_stations_per_side * 2:
            max_stations = max_stations_per_side * 2
        else:
            max_stations = len(stations)
        left_stations  = sorted(stations[max_stations_per_side:max_stations],
            key=lambda station: station.numerical_name(), reverse=True)
        right_stations = sorted(stations[:max_stations_per_side],
            key=lambda station: station.numerical_name(), reverse=True)
        d = {
            'left_stations' : left_stations,
            'right_stations': right_stations,
        }
    return render_to_response('schedules/root.html', d, 
        context_instance=RequestContext(request))

@login_required
def task(request, pk):
    """Create task and assign job to employees."""
    schedule = get_object_or_404(Schedule, pk=pk)
    if settings.DEV:
        set_task(schedule)
        messages.success(request, 'Tasks set')
    else:
        # Place in queue to run in the background
        django_rq.enqueue(set_task, schedule)
        messages.success(request, 'Setting tasks, please wait')
    return HttpResponseRedirect(reverse('schedules.views.detail', 
        args=[schedule.pk]))