# file: restaurant/views.py
# Author: Evren Yaman (yamane@bu.edu), 9/16/2025
# Description: This file creates requests for all three pages in the restaurant/urls.py file, and it renders the pages with the necessary context.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.

pricing = {
    "Special": 10,
    "House Steamed Crab": 38,
    "La-Zi Chicken (Mild)": 21,
    "La-Zi Chicken (Medium)": 21,
    "La-Zi Chicken (Spicy)": 21,
    "Hot Spicy Pork Kidney": 24,
    "Ma-La Lobster": 47,
}

specials = [
    "Szechuan Pickles",
    "House Chicken",
    "Ma-Po Tofu",
    "Green Spicy Bass",
]

def main(request):
    '''Function to respond to the "main" request.
    '''

    template_name = 'restaurant/main.html'

    # Gets the current time
    current_time = time.ctime()

    context = {
        "time": current_time,
    }

    return render(request, template_name, context)

def order(request):
    '''Function to respond to the "order" request. Will show the form to the user.
    '''

    template_name = 'restaurant/order.html'

    # Gets the current time
    current_time = time.ctime()

    context = {
        "time": current_time,
        "special": specials[random.randint(1,4)-1]
    }

    return render(request, template_name, context)

def confirmation(request):
    '''Function to respond to the order form submission, and renders the results.
    '''

    template_name = 'restaurant/confirmation.html'
    print(request.POST)

    # Gets the current time
    current_time = time.ctime()

    # Randomly generates the expected time at which the order will be ready
    ready = time.time() + (random.randint(30, 60) * 60)
    readytime = time.ctime(ready)

    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        items = request.POST.getlist('item')
        total = 0
        for item in items:
            total += pricing[item]
        
        allergies = request.POST['allergies']
        instructions = request.POST['instructions']


        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'items': items,
            'allergies': allergies,
            'instructions': instructions,
            "time": current_time,
            "readytime": readytime,
            "total": total,
        }

    return render(request, template_name=template_name, context=context)
