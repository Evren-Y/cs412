# file: restaurant/views.py
# Author: Evren Yaman (yamane@bu.edu), 9/16/2025
# Description: This file creates requests for all three pages in the restaurant/urls.py file, and it renders the pages with the necessary context.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.

specials = [
    "Szechuan Pickles",
    "House Chicken",
    "Ma-Po Tofu",
    "Green Spicy Bass",
]

# Gets the current time
time = time.ctime()

# Randomly generates the expected time at which the order will be ready
readytime = time

def main(request):
    '''Function to respond to the "main" request.
    '''

    template_name = 'restaurant/main.html'

    context = {
        "time": time,
    }

    return render(request, template_name, context)

def order(request):
    '''Function to respond to the "order" request. Will show the form to the user.
    '''

    template_name = 'restaurant/order.html'

    context = {
        "time": time,
        "special": specials[random.randint(1,4)-1]
    }

    return render(request, template_name, context)

def confirmation(request):
    '''Function to respond to the order form submission, and renders the results.
    '''

    template_name = 'restaurant/confirmation.html'
    print(request.POST)

    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        items = request.POST.getlist('item')
        
        allergies = request.POST['allergies']
        instructions = request.POST['instructions']


        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'items': items,
            'allergies': allergies,
            'instructions': instructions,
            "time": time,
        }

    return render(request, template_name=template_name, context=context)
