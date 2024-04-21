from django.contrib import admin
from django.urls import path
from .import views 
from django.contrib.auth import views as auth_views
from myapp import views as user_views


urlpatterns = [
    path('', views.index,name='index'),
    path('edit/<int:id>/',views.edit,name='edit'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='myapp/login.html'),name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('invalid/',views.invalid,name='invalid'),
]