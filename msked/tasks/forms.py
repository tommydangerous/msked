from django import forms
from django.forms import ModelForm
from employees.models import Employee
from tasks.models import Task

class TaskForm(ModelForm):
    class Meta:
        model  = Task
        fields = ('job',)

class TaskEditForm(ModelForm):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all().order_by('last_name'))

    class Meta:
        model  = Task
        fields = ('employee', 'job',)