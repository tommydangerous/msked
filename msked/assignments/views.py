from assignments.models import Assignment
from assignments.forms import AssignmentForm, AssignmentEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from employees.models import Employee
from msked.utils import add_csrf

@login_required
def new(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    item = 'seats'
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.employee = employee
            assignment.save()
            messages.success(request, 'Assignment created')
            return HttpResponseRedirect(reverse('employees.views.history', 
                kwargs={ 'slug': employee.slug, 'item': item }))
    else:
        form = AssignmentForm()
    d = {
        'employee': employee,
        'form'    : form,
        'item'    : item,
        'title'   : 'New Assignment',
    }
    return render_to_response('shared/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    item = 'seats'
    if request.method == 'POST':
        form = AssignmentEditForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, 'Assignment updated')
            return HttpResponseRedirect(reverse('employees.views.history', 
                kwargs={ 'slug': assignment.employee.slug, 'item': item }))
    else:
        form = AssignmentEditForm(instance=assignment)
    d = {
        'employee': assignment.employee,
        'form'    : form,
        'item'    : item,
        'title'   : 'Edit Assignment',
    }
    return render_to_response('shared/new.html', add_csrf(request, d),
        context_instance=RequestContext(request))