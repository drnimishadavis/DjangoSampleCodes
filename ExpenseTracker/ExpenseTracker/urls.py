
from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',IndexView.as_view(),name="index"),
    path('register/',SignUpView.as_view(),name="register"),
    path('signin/',SignInView.as_view(),name="signin"),
    path('home/',HomeView.as_view(),name="home"),
    path("signout/", SignoutView.as_view(), name="signout"),
    path('expense/add/',AddExpense.as_view(),name="addexpense"),
    path('expense/<int:id>/edit/', EditExpense.as_view(), name='editexpense'),
    path('expense/<int:id>/delete/', DeleteExpense.as_view(), name='deleteexpense'),
    path('expense/<int:id>/', DetailExpense.as_view(), name='expensedetail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
