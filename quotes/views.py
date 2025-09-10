# file: hw/view.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.
quotes = [
    "Never interrupt your enemy when he is making a mistake.",
    "I start out by believing the worst.",
    "There are only two forces that unite men - fear and interest.",
    "The best way to keep one's word is not to give it.",
]

images = [
    "quotes/napoleon_one.jpg",
    "quotes/napoleon_two.jpg",
    "quotes/napoleon_three.jpg",
    "quotes/napoleon_four.jpg",
]

time = time.ctime()

def home_page(request):
    '''Function to respond to the "home" request.'''

    template_name = 'quotes/home.html'
    context = {
        "quote": quotes[random.randint(1,4)-1],
        "image": images[random.randint(1,4)-1],
        "time": time,
    }
    return render(request, template_name, context)

def quote(request):
    '''Function to respond to the "quote" request.'''

    template_name = 'quotes/quote.html'
    context = {
        "quote": quotes[random.randint(1,4)-1],
        "image": images[random.randint(1,4)-1],
        
    }
    return render(request, template_name, context)

def show_all(request):
    '''Function to respond to the "show_all" request.'''

    template_name = 'quotes/show_all.html'
    context = {
        "quotes": quotes,
        "images": images,
        "time": time,
    }
    return render(request, template_name, context)

def about(request):
    '''Function to respond to the "about" request.'''

    template_name = 'quotes/about.html'
    context = {
        "time": time,
    }
    return render(request, template_name, context)
