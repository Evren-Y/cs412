# file: restaurant/urls.py
# Author: Evren Yaman (yamane@bu.edu), 9/16/2025
# Description: extension of cs412 urls.py file, creating the paths for all pages used in the restaurant web application.

from django.urls import path
from django.conf import settings
from . import views

#URL patterns specific to the quotes app:
urlpatterns = [
    path(r'', views.main, name="main_page"),
    path(r'order', views.order, name="order_page"),
    path(r'confirmation', views.confirmation, name="confirmation_page"),
]