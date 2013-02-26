from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from employees.forms import EmployeeForm
from employees.models import Employee
from msked.utils import add_csrf, page

@login_required
def list(request):
    q = request.GET.get('q', '')
    if q:
        all_emp = Employee.objects.filter(
            Q(first_name__icontains=q) | Q(
                last_name__icontains=q)).order_by('last_name')
    else:
        all_emp = Employee.objects.all().order_by('last_name')
    emp_count = all_emp.count()
    employees = page(request, all_emp, 20)
    d = {
        'emp_count': emp_count,
        'objects'  : employees,
        'q'        : q,
        'title'    : 'Employees',
    }
    return render_to_response('employees/list.html', d, 
        context_instance=RequestContext(request))

@login_required
def new(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        print '%s' % form.is_valid()
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee created')
            return HttpResponseRedirect(reverse('employees.views.detail', 
                args=[employee.slug]))
    else:
        form = EmployeeForm()
    d = {
        'form'    : form,
        'title'   : 'New Employee',
    }
    return render_to_response('employees/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))


@login_required
def detail(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    assignments = employee.assignment_set.all().order_by('-created')[:5]
    placements = employee.placement_set.all().order_by('-created')[:5]
    tasks = employee.task_set.all().order_by('-created')[:5]
    d = {
        'assignments': assignments,
        'employee'   : employee,
        'placements' : placements,
        'tasks'      : tasks,
        'title'      : '%s %s' % (employee.first_name, employee.last_name),
    }
    return render_to_response('employees/detail.html', d, 
        context_instance=RequestContext(request))

@login_required
def edit(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, 'Employee updated')
            return HttpResponseRedirect(reverse('employees.views.detail', 
                args=[employee.slug]))
    else:
        form = EmployeeForm(instance=employee)
    d = {
        'employee': employee,
        'form'    : form,
        'title'   : 'Edit Employee',
    }
    return render_to_response('employees/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def history(request, slug, item):
    employee = get_object_or_404(Employee, slug=slug)
    if item == 'jobs':
        objects = employee.task_set.all().order_by('-created')
        url = reverse('tasks.views.new', args=[employee.slug])
    elif item == 'locations':
        objects = employee.placement_set.all().order_by('-created')
        url = reverse('placements.views.new', args=[employee.slug])
    elif item == 'seats':
        objects = employee.assignment_set.all().order_by('-created')
        url = reverse('assignments.views.new', args=[employee.slug])
    d = {
        'count'   : objects.count(),
        'employee': employee,
        'item'    : item,
        'objects' : page(request, objects, 20),
        'title'   : "%s's %s" % (employee.first_name, item.capitalize()),
        'url'     : url,
    }
    return render_to_response('employees/history.html', d, 
        context_instance=RequestContext(request))

@login_required
def notes(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    item = 'notes'
    q = request.GET.get('q', '')
    if q:
        all_notes = employee.note_set.filter(
            content__icontains=q).order_by('-updated')
    else:
        all_notes = employee.note_set.all().order_by('-updated')
    d = {
        'count'   : all_notes.count(),
        'employee': employee,
        'item'    : item,
        'objects' : page(request, all_notes, 20),
        'q'       : q,
        'title'   : '%s Notes' % employee.first_name,
    }
    return render_to_response('employees/notes.html', d, 
        context_instance=RequestContext(request))