from django import forms
from django.forms import ModelForm
from employees.models import Employee
from placements.models import Placement

class PlacementForm(ModelForm):
    class Meta:
        model  = Placement
        fields = ('location',)

class PlacementEditForm(ModelForm):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all().order_by('last_name'))
    
    class Meta:
        model  = Placement
        fields = ('employee', 'location',)