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
from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    url(r'^list(\d+)_(\d+)_(\d+)/', list, name='list'),
    url(r'^immedi_buy(\d+)_(\d+)/', immedi_buy, name='immedi_buy'),
    url(r'^add_cart(\d+)_(\d+)/', add_cart, name='add_cart'),
    path('show_cart/', show_cart, name='show_cart'),
    url(r'^(\d+)/', detail, name='detail'),
    url(r'^delete_cart/(\d+)', delete_cart, name='delete_cart')
]
