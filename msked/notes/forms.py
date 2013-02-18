from django import forms
from django.forms import ModelForm
from notes.models import Note

class NoteForm(ModelForm):
    class Meta:
        model  = Note
        fields = ('content',)