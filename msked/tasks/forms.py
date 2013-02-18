from django import forms
from django.forms import ModelForm
from tasks.models import Task

class TaskForm(ModelForm):
    class Meta:
        model  = Task
        fields = ('job',)

class TaskEditForm(ModelForm):
    class Meta:
        model  = Task
        fields = ('employee', 'job',)