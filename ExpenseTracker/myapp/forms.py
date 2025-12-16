from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from myapp.models import *
# class SignUpForm(UserCreationForm):
#     class Meta:
#         model=User
#         fields=["username","email","password1","password2"]

# class SigninForm(forms.Form):
#     username=forms.CharField()
#     password=forms.CharField(widget=forms.PasswordInput())


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})
    )


class SigninForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )


class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        fields=["title","amount","category", "bill_image"]
        # exclude=("Created_at,owner")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter title"
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter amount"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
        }
