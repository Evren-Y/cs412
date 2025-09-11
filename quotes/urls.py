# file: quotes/urls.py
# Author: Evren Yaman (yamane@bu.edu), 9/11/2025
# Description: extension of cs412 urls.py file, creating the paths for all pages used in the quotes web application.

from django.urls import path
from django.conf import settings
from . import views

#URL patterns specific to the quotes app:
urlpatterns = [
    path(r'', views.home, name="home_page"),
    path(r'quote', views.quote, name="quote_page"),
    path(r'show_all', views.show_all, name="show_all_page"),
    path(r'about', views.about, name="about_page"),
]