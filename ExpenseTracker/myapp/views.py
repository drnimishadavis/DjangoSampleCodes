from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from myapp.forms import SignUpForm,SigninForm,ExpenseForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from myapp.models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from .models import Expense
from django.contrib import messages
import calendar

from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Expense
import datetime
import json


def _shift_months(source_date: datetime.date, offset: int) -> datetime.date:
    month = source_date.month - 1 + offset
    year = source_date.year + month // 12
    month = month % 12 + 1
    return datetime.date(year, month, 1)

class IndexView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            context = {
                "total_expense": 0,
                "category_labels": [],
                "category_values": [],
                "month_labels": [],
                "month_values": [],
                "month_total": 0,
                "category_count": 0,
                "recent_expenses": [],
            }
            return render(request, self.template_name, context)

        qs = Expense.objects.filter(owner=user)

        total = qs.aggregate(total=Sum("amount"))["total"] or 0

        # By category
        by_cat_qs = qs.values("category").annotate(total=Sum("amount")).order_by("-total")
        category_labels = [item["category"] for item in by_cat_qs]
        category_values = [item["total"] or 0 for item in by_cat_qs]

        # Last 12 months
        today = datetime.date.today()
        first_of_this_month = today.replace(day=1)

        month_qs = (
            qs.annotate(month=TruncMonth("created_at"))
              .values("month")
              .annotate(total=Sum("amount"))
              .order_by("month")
        )
        month_map = {}
        for item in month_qs:
            if item["month"] is None:
                continue
            month_map[item["month"].date()] = item["total"] or 0

        month_labels = []
        month_values = []
        for offset in range(-11, 1):
            mdate = _shift_months(first_of_this_month, offset)
            month_labels.append(mdate.strftime("%b %Y"))
            month_values.append(month_map.get(mdate, 0))

        month_total = sum(month_values)
        category_count = len(category_labels)

        # ✅ Recent 6 expenses
        recent_expenses = qs.order_by('-created_at')[:6]

        context = {
            "total_expense": total,
            "category_labels": category_labels,
            "category_values": category_values,
            "month_labels": month_labels,
            "month_values": month_values,
            "month_total": month_total,
            "category_count": category_count,
            "recent_expenses": recent_expenses,
        }

        return render(request, self.template_name, context)


# class IndexView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,"index.html")
    

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form_instance=SignUpForm()
        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=SignUpForm(form_data)
        if form_instance.is_valid():
            # data=form_instance.cleaned_data
            # User.objects.create_user(**data)
            form_instance.save()
            return redirect("signin")
        else:
            print("Error occured.")
            return render(request,"register.html",{"form":form_instance})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form_instance=SigninForm()
        return render(request,"login.html",{"forms":form_instance})
    
    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=SigninForm(form_data)
        if form_instance.is_valid():
            data=form_instance.cleaned_data #it will be a dictionary
            uname=data.get("username")
            pwd=data.get("password")
            user_instance=authenticate(request,username=uname,password=pwd)
            if user_instance:
                login(request,user_instance)
                print("login success")
                return redirect("index")
            else:
                print("failed")
                return render(request,"login.html",{"forms":form_instance})

class SignoutView(View):
    def get(self, request,*args,**kwargs):
        logout(request)
        return redirect("signin") 


class HomeView(LoginRequiredMixin,View):
    login_url = 'signin'       
    redirect_field_name = 'next'
    def get(self,request,*args,**kwargs):
        expenses = Expense.objects.filter(owner=request.user).order_by('-created_at')
        total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        return render(request, "home.html", {
            "expenses": expenses,
            "total_amount": total_amount
        })

@method_decorator(login_required(login_url='signin'), name='dispatch')
class AddExpense(View):
    def get(self,request,*args,**kwargs):
        form_instance=ExpenseForm()
        expenses = Expense.objects.filter(owner=request.user).order_by('-created_at')
        total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        return render(request,"expense_add.html",{
            "form": form_instance,
            "expenses": expenses,
            "total_amount": total_amount
        })

    def post(self,request,*args,**kwargs):
        form_instance=ExpenseForm(request.POST, request.FILES)
        if form_instance.is_valid():
            expense = form_instance.save(commit=False)
            expense.owner = request.user
            expense.save()
            return redirect('addexpense')
        else:
            return render(request,"expense_add.html",{"form":form_instance})
@method_decorator(login_required(login_url='signin'), name='dispatch')
class EditExpense(View):
    def get(self, request, *args, **kwargs):
        expense_id = kwargs.get("id")
        expense_obj = get_object_or_404(Expense, id=expense_id)

        # Ownership check
        if expense_obj.owner != request.user:
            return HttpResponseForbidden("You do not have permission to edit this expense.")

        form = ExpenseForm(instance=expense_obj)
        return render(request, "edit_expense.html", {"form": form, "expense": expense_obj})

    def post(self, request, *args, **kwargs):
        expense_id = kwargs.get("id")
        expense_obj = get_object_or_404(Expense, id=expense_id)

        # Ownership check
        if expense_obj.owner != request.user:
            return HttpResponseForbidden("You do not have permission to edit this expense.")

        # Handle file uploads
        form = ExpenseForm(request.POST, request.FILES, instance=expense_obj)
        if form.is_valid():
            form.save()
            return redirect("home")

        return render(request, "edit_expense.html", {"form": form, "expense": expense_obj})

@method_decorator(login_required(login_url='signin'), name='dispatch')
class DeleteExpense(View):
    def post(self, request, *args, **kwargs):
        expense_id = kwargs.get("id")
        expense = get_object_or_404(Expense, id=expense_id)
        if expense.owner != request.user:
            return HttpResponseForbidden("You do not have permission to delete this expense.")
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
        return redirect("home")
    def get(self, request, *args, **kwargs):
        return redirect("home")
    
@method_decorator(login_required(login_url='signin'), name='dispatch')
class DetailExpense(View):
    def get(self, request, *args, **kwargs):
        expense_id = kwargs.get("id")
        expense = get_object_or_404(Expense, id=expense_id)
        if expense.owner != request.user:
            return HttpResponseForbidden("You do not have permission to view this expense.")
        return render(request, "expensedetail.html", {"expense": expense})
    
