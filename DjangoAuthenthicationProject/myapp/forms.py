from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","first_name","last_name","password"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()