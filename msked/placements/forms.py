from django import forms
from django.forms import ModelForm
from placements.models import Placement

class PlacementForm(ModelForm):
    class Meta:
        model  = Placement
        fields = ('location',)

class PlacementEditForm(ModelForm):
    class Meta:
        model  = Placement
        fields = ('employee', 'location',)