from django.urls import path
from .views import *
urlpatterns = [
    path('',HomeView.as_view(),name="index"),
    path('addbook/',AddBookView.as_view(),name="addbook"),
    path('bookdetails/<int:pk>',BookDetailView.as_view(),name="bookdetails"),
    path('bookdelete/<int:pk>',BookDeleteView.as_view(),name="bookdelete"),
    path('bookupdata/<int:pk>',BookEditView.as_view(),name="bookupdate"),
    path('profile',ProfileAdd.as_view(),name="profile"),
    path("update/<int:id>/", ProfileUpdateView.as_view(), name="update-profile")

    
]