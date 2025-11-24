from django import forms
from bookapp.models import *

class BookForm(forms.Form):
    title=forms.CharField()
    author=forms.CharField()
    price=forms.IntegerField()
    genre=forms.CharField()
    language=forms.CharField()
    year=forms.CharField()

# ModelForm
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        # fields=["name","email","password"]
        fields="__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
        }