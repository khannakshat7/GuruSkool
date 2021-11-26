from django import forms
from django.contrib.auth.models import User


# User form to accept and validate user credentials for login and registration
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')
