from assignments.models import Assignment
from django import forms
from django.forms import ModelForm

class AssignmentForm(ModelForm):
    class Meta:
        model  = Assignment
        fields = ('seat',)

class AssignmentEditForm(ModelForm):
    class Meta:
        model  = Assignment
        fields = ('employee', 'seat')