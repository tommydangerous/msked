from assignments.models import Assignment
from django import forms
from django.forms import ModelForm
from employees.models import Employee

class AssignmentForm(ModelForm):
    class Meta:
        model  = Assignment
        fields = ('seat',)

class AssignmentEditForm(ModelForm):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all().order_by('last_name'))
    
    class Meta:
        model  = Assignment
        fields = ('employee', 'seat')