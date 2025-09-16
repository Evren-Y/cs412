# file: restaurant/views.py
# Author: Evren Yaman (yamane@bu.edu), 9/16/2025
# Description: This file creates requests for all three pages in the restaurant/urls.py file, and it renders the pages with the necessary context.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.

# Gets the current time
time = time.ctime()

# Randomly generates the expected time at which the order will be ready
readytime = time

def main(request):
    '''Function to respond to the "main" request.
    '''

    template_name = 'restaurant/main.html'

    return render(request, template_name)

def order(request):
    '''Function to respond to the "order" request.
    '''

    template_name = 'restaurant/order.html'

    return render(request, template_name)

def confirmation(request):
    '''Function to respond to the "show_all" request.
    '''

    template_name = 'restaurant/confirmation.html'

    return render(request, template_name)
