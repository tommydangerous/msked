from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import timezone

from employees.models import Employee
from msked.utils import add_csrf
from notes.forms import NoteForm
from notes.models import Note
from stations.models import Station

@login_required
def new(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.employee = employee
            note.user = request.user
            note.updated = timezone.now()
            note.save()
            messages.success(request, 'Note created')
            return HttpResponseRedirect(reverse('employees.views.notes', 
                args=[employee.slug]))
    form = NoteForm()
    d = {
        'employee': employee,
        'form'    : form,
        'title'   : 'New Note',
    }
    return render_to_response('shared/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.updated = timezone.now()
            note.save()
            messages.success(request, 'Note updated')
            if note.employee:
                return HttpResponseRedirect(reverse('employees.views.notes', 
                    args=[note.employee.slug]))
            elif note.station:
                return(HttpResponseRedirect(reverse('stations.views.detail',
                    args=[note.station.slug])))
    form = NoteForm(instance=note)
    d = {
        'employee': note.employee,
        'form'    : form,
        'station' : note.station,
        'title'   : 'Edit Note',
    }
    return render_to_response('shared/new.html', add_csrf(request, d),
        context_instance=RequestContext(request))

@login_required
def station(request, slug):
    """Add a note for a station."""
    station = get_object_or_404(Station, slug=slug)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.station = station
            note.user    = request.user
            note.updated = timezone.now()
            note.save()
            messages.success(request, 'Note created')
            return HttpResponseRedirect(reverse('stations.views.detail',
                args=[station.slug]))
    form = NoteForm()
    d = {
        'form': form,
        'station': station,
        'title': 'New Note',
    }
    return render_to_response('shared/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))