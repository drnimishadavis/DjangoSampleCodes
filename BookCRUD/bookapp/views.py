from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from .models import Book
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import *


class HomeView(View):
    def get(self,request,*args,**kwargs):
        query=request.GET.get("q")
        books = Book.objects.all()
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        return render(request,"index.html",{"books": books})

class AddBookView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"addbook.html")
    def post(self,request,*args,**kwargs):
        form_data = request.POST
        image = request.FILES.get("image")  
        Book.objects.create(
            title=form_data.get("title"),
            author=form_data.get("author"),
            price=form_data.get("price"),
            language=form_data.get("language"),
            genre=form_data.get("genre"),
            year=form_data.get("year"),
            image=image   
        )

        return redirect("index")
       

# BookDetailView
# url : localhost:8000/books/{id}
# method : GET
class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        book=Book.objects.get(id=id)
        return render(request,"book_detail.html",{"books":book})
    
# BookEditView
class BookEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        book=Book.objects.get(id=id)
        return render(request,"updatebook.html",{"books":book})
    
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        book = Book.objects.get(id=id)
    # Update normal fields only
        for key, value in request.POST.items():
            if key in ["csrfmiddlewaretoken", "image"]:
                continue
            setattr(book, key, value)
    # Only replace image if a file is selected
        if request.FILES.get("image"):
            book.image = request.FILES["image"]
        book.save()
        return redirect("index")

    
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Book.objects.get(id=id).delete()
        return redirect("index")
    

from django.views import View
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile

class ProfileAdd(View):
    def get(self, request):
        form = ProfileForm()
        profiles = Profile.objects.all()   # fetch all rows
        return render(request, "profile.html", {"form": form, "profiles": profiles})

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile")

        profiles = Profile.objects.all()
        return render(request, "profile.html", {"form": form, "profiles": profiles})

class ProfileUpdateView(View):
    def get(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        form = ProfileForm(instance=profile)
        return render(request, "update_profile.html", {"form": form, "profile": profile})

    def post(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")   # redirect to list page or success
        return render(request, "update_profile.html", {"form": form, "profile": profile})