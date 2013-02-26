from assignments.utils import assign_seating
from collections import defaultdict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from placements.utils import set_placements, switch_placements
from schedules.models import Schedule
from tasks.utils import set_task

@login_required
def root(request):
    schedule = Schedule.objects.all().order_by('created')[0]
    location = schedule.locations_by_occupancy()[0]
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
def detail(request, pk):
    """Schedule detail page."""
    schedule = get_object_or_404(Schedule, pk=pk)
    d = {
        'jobs'     : schedule.jobs(),
        'locations': schedule.locations(),
        'schedule' : schedule,
        'title'    : schedule.name,
    }
    return render_to_response('schedules/detail.html', d, 
        context_instance=RequestContext(request))

@login_required
def assignment(request, pk):
    """Create assignment for station seating for employees."""
    schedule = get_object_or_404(Schedule, pk=pk)
    assign_seating(schedule)
    messages.success(request, 'Seating assigned')
    return HttpResponseRedirect(reverse('root_path'))

@login_required
def placement(request, pk):
    """Create placement and set/switch locations for employees."""
    schedule = get_object_or_404(Schedule, pk=pk)
    if switch_placements(schedule):
        messages.success(request, 'Placements switched')
    else:
        messages.error(request, 'Nothing was done, loop exceeded maximum')
    return HttpResponseRedirect(reverse('schedules.views.detail', 
        args=[schedule.pk]))

@login_required
def task(request, pk):
    """Create task and assign job to employees."""
    schedule = get_object_or_404(Schedule, pk=pk)
    set_task(schedule)
    messages.success(request, 'Tasks set')
    return HttpResponseRedirect(reverse('schedules.views.detail', 
        args=[schedule.pk]))