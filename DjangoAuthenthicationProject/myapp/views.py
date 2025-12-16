from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.forms import SignupForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

class Index(View):
    def get(self,request,*args,**kwargs):
        return render(request,"index.html")
    
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form_instance=SignupForm()
        return render(request,"signup.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=SignupForm(form_data)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            # User.objects.create(**data)
            User.objects.create_user(**data)
            print("Ac created")
            return redirect("signin")
        print("Signup Failed")
        return render(request,"signup.html",{"form":form_instance})

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form_instace=LoginForm()
        return render(request,"login.html",{"form":form_instace})
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=LoginForm(form_data)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                print("valid")
                # session
                login(request,user_object)
                print(request.user)
                print("Session started")


            else:
                print("invalid")
            # print(uname,pwd)
            # user_instance=User.objects.get(username=uname)
            # if user_instance.check_password(pwd):

            #     print("credentials are valid.")
            # else:
            #     print("Credentials are invalid.")
            #     return redirect("signin")
            return redirect("profile")


class ProfileView(LoginRequiredMixin,View):
    login_url = 'signin'
    def get(self,request,*args,**kwargs):
        return render(request,"profile.html")
    
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("index")