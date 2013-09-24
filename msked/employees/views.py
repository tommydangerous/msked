from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext

from employees.forms import EmployeeForm
from employees.models import Employee
from employees.utils import remove_local_images, s3_upload
from msked.utils import add_csrf, pacific_date, page

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
            # Process image
            image = request.FILES.get('image')
            if image:
                employee.image = image
                employee.save()
                s3_upload(employee)
                remove_local_images()
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

@login_required
def timeline(request, slug):
    """Show employee's jobs, locations, notes, and seats on 1 page."""
    employee    = get_object_or_404(Employee, slug=slug)
    assignments = [x for x in employee.assignment_set.order_by('-created')]
    notes       = [x for x in employee.note_set.order_by('-created')]
    placements  = [x for x in employee.placement_set.order_by('-created')]
    tasks       = [x for x in employee.task_set.order_by('-created')]
    objects     = assignments + notes + placements + tasks 
    objects.sort(key=lambda x: x.created, reverse=True)
    # Group objects by date
    if objects:
        dates = set([pacific_date(obj.created) for obj in objects])
        dates = sorted(dates, key=lambda x: datetime.strptime(x, '%b %d, %y'),
            reverse=True)
        days = []
        for day in dates:
            objs = [obj for obj in objects if pacific_date(obj.created) == day]
            days.append((day, objs))
    d = {
        'days': days,
        'employee': employee,
        'title': '%s\'s Timeline' % employee.first_name,
    }
    return render(request, 'employees/timeline.html', d)