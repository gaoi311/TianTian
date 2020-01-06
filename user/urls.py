"""TianTian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('register_handler/', register_handler, name='register_handler'),
    path('register_exist/', register_exist),
    path('login/', login, name='login'),
    path('login_handler/', login_handler, name='login_handler'),
    path('info/', info, name='info'),
    path('order/', order, name='order'),
    path('site/', site, name='site'),
    path('surprise_view/', surprise_view, name='surprise')
]
