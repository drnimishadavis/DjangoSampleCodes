from django.contrib import admin
from django.urls import path,include

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.Index.as_view(),name="index"),
    path("register/",views.SignUpView.as_view(),name="register"),
    path("signin/",views.LoginView.as_view(),name="signin"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("signout/",views.SignoutView.as_view(),name="signout"),
    
    
]
