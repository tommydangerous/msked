from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from employees.models import Employee
from msked.utils import add_csrf
from schedules.models import Schedule
from requires.models import Require
from tasks.forms import TaskForm, TaskEditForm
from tasks.models import Task
from works.models import Work

@login_required
def new(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    item = 'jobs'
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.employee = employee
            task.save()
            try:
                work = employee.work_set.get(job=task.job)
            except ObjectDoesNotExist:
                employee.work_set.create(job=task.job)
            messages.success(request, 'Task created')
            return HttpResponseRedirect(reverse('employees.views.history', 
                kwargs={ 'slug': employee.slug, 'item': item }))
    form = TaskForm()
    d = {
        'employee': employee,
        'form'    : form,
        'item'    : item,
        'title'   : 'New Task',
    }
    return render_to_response('shared/new.html', add_csrf(request, d), 
        context_instance=RequestContext(request))

@login_required
def edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    old_employee = task.employee
    old_job = task.job
    item = 'jobs'
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            # if employee changed
            if task.employee.pk != old_employee.pk:
                # delete old employee old job
                try:
                    work = old_employee.work_set.get(job=old_job)
                    work.delete()
                except ObjectDoesNotExist:
                    pass
                # create task employee task job
                try:
                    work = task.employee.work_set.get(job=task.job)
                except ObjectDoesNotExist:
                    task.employee.work_set.create(job=task.job)
            # if job changed
            elif task.job.pk != old_job.pk:
                # delete task employee old job
                try:
                    work = task.employee.work_set.get(job=old_job)
                    work.delete()
                except ObjectDoesNotExist:
                    pass
                # create task employee task job
                try:
                    work = task.employee.work_set.get(job=task.job)
                except ObjectDoesNotExist:
                    task.employee.work_set.create(job=task.job)
            messages.success(request, 'Task updated')
            return HttpResponseRedirect(reverse('employees.views.history', 
                kwargs={ 'slug': task.employee.slug, 'item': item }))
    form = TaskEditForm(instance=task)
    d = {
        'employee': task.employee,
        'form'    : form,
        'item'    : item,
        'title'   : 'Edit Task',
    }
    return render_to_response('shared/new.html', add_csrf(request, d),
        context_instance=RequestContext(request))

@login_required
def delete_all(request):
    Require.objects.all().delete()
    Task.objects.all().delete()
    Work.objects.all().delete()
    messages.success(request, 'Tasks deleted')
    return HttpResponseRedirect(reverse('schedules.views.detail', 
        args=[Schedule.objects.all()[0].pk]))