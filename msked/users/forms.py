from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

import re

class UserEditForm(ModelForm):
    email = forms.EmailField(label='Email', 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off' }))
    password1 = forms.CharField(label='Password', required=False, 
        widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password confirmation', required=False, 
        widget=forms.PasswordInput())
    username = forms.CharField(label='Full name', max_length=30, 
        widget=forms.TextInput(attrs={ 'autocomplete': 'off' }))

    class Meta:
        model  = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email:
            email = email.lower()
        return email

    def clean_password2(self):
        """Validate password1 and password2 matches."""
        error_message = 'Password confirmation does not match'
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError(error_message)
        elif password2 and password1 != password2:
            raise forms.ValidationError(error_message)
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        pattern = re.compile(r'^[-A-Za-z]{2,} [-A-Za-z]{2,}$')
        if re.search(pattern, username):
            first_name, last_name = username.split()
            first_name = first_name.lower().capitalize()
            last_name = last_name.lower().capitalize()
            username = '%s %s' % (first_name, last_name)
        else:
            raise forms.ValidationError('Please enter your full name')
        return username

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        # split username into first and last name
        first_name, last_name = self.cleaned_data.get('username').split()
        # save user
#        user.email = self.cleaned_data.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.username = '%s %s' % (first_name, last_name)
        # if user changed password
        password2 = self.cleaned_data.get('password2')
        if password2:
            user.set_password(password2)
        if commit:
            user.save()
        return user