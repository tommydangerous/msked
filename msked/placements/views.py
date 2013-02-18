from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from employees.models import Employee
from msked.utils import add_csrf
from placements.forms import PlacementForm, PlacementEditForm
from placements.models import Placement
from schedules.models import Schedule

@login_required
def new(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    item = 'locations'
    if request.method == 'POST':
        form = PlacementForm(request.POST)
        if form.is_valid():
            placement = form.save(commit=False)
            placement.employee = employee
            placement.save()
            messages.success(request, 'Placement created')
            return HttpResponseRedirect(reverse('employees.views.history', 
                kwargs={ 'slug': employee.slug, 'item': item }))
    form = PlacementForm()
    d = {
        'employee': employee,
        'form'    : form,
        'item'    : item,
        'title'   : 'New Placement',
    }
    return render_to_response('shared/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def edit(request, pk):
    placement = get_object_or_404(Placement, pk=pk)
    item = 'locations'
    if request.method == 'POST':
        form = PlacementEditForm(request.POST, instance=placement)
        if form.is_valid():
            placement = form.save()
            messages.success(request, 'Placement updated')
            return HttpResponseRedirect(reverse('employees.views.history', 
                kwargs={ 'slug': placement.employee.slug, 'item': item }))
    form = PlacementEditForm(instance=placement)
    d = {
        'employee': placement.employee,
        'form'    : form,
        'item'    : item,
        'title'   : 'Edit Placement',
    }
    return render_to_response('shared/new.html', add_csrf(request, d),
        context_instance=RequestContext(request))

@login_required
def delete_all(request):
    Placement.objects.all().delete()
    messages.success(request, 'Placements deleted')
    return HttpResponseRedirect(reverse('schedules.views.detail', 
        args=[Schedule.objects.all()[0].pk]))