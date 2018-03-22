from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
    )


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username