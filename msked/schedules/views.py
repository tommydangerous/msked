from assignments.utils import assign_seating
from collections import defaultdict
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, RequestContext
from placements.utils import set_placements, switch_placements
from schedules.models import Schedule
from tasks.utils import set_task

import django_rq
import json

@login_required
def assignment(request, pk):
    """Create assignment for station seating for employees."""
    schedule = get_object_or_404(Schedule, pk=pk)
    assign_seating(schedule)
    messages.success(request, 'Seating assigned')
    return HttpResponseRedirect(reverse('root_path'))

@login_required
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

@login_required
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

@login_required
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

@login_required
def root(request):
    schedule = Schedule.objects.all().order_by('created')[0]
    location_schedule = schedule.locationschedule_set.filter(
        location__name__icontains='lab')
    d = {}
    if location_schedule:
        location = location_schedule[0].location
        stations = location.stations()
        if len(stations) > 8:
            max_station = 8
        else:
            max_station = len(stations)
        left  = sorted(stations[6:max_station], 
            key=lambda s: s.name, reverse=True)
        right = sorted(stations[:6], key=lambda s: s.name, reverse=True)
        reject = [s for s in stations if s.name == 'Rejects']
        wet_copies = [s for s in stations if s.name == 'Wet Copies']
        d = {
            'left'      : left,
            'right'     : right,
            'reject'    : reject,
            'wet_copies': wet_copies,
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