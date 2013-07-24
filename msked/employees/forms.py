from django import forms
from django.forms import ModelForm
from employees.models import Employee

class EmployeeForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={ 'autocomplete': 'off' }))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={ 'autocomplete': 'off' }))
    tier_lab = forms.CharField(widget=forms.TextInput(
        attrs={ 'autocomplete': 'off' }))
    tier_office = forms.CharField(widget=forms.TextInput(
        attrs={ 'autocomplete': 'off' }), required=False)
    
    class Meta:
        model  = Employee
        fields = ('first_name', 'last_name', 'tier_lab', 'tier_office', 
            'team', 'floater', 'vacation',)

    def clean_tier_office(self):
        tier = self.cleaned_data.get('tier_office')
        if tier:
            return tier
        else:
            return None