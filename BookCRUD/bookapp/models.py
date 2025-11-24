from django.db import models
from django import forms

# Book [ id, title, author, price, language, genre, year]
class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=250)
    price=models.PositiveIntegerField()
    language=models.CharField(max_length=200)
    genre=models.CharField(max_length=100)
    year=models.CharField(max_length=10)
    image = models.ImageField(upload_to="book_images/", null=True, blank=True)
    # overriding str method : to print the title name only
    def __str__(self):
        return self.title
    
class Profile(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=300)

