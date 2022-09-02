from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib import admin

app_name = 'app'

urlpatterns = [
    path('', TaskView.as_view(), name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
 ]
