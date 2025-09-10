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
    "https://dreamsinparis.com/wp-content/uploads/2022/08/Painting-of-Napoleon-873x1024.jpg",
    "https://dreamsinparis.com/wp-content/uploads/2023/05/Napoleons-retreat-from-moscow-1024x780.jpg",
    "https://dreamsinparis.com/wp-content/uploads/2023/05/Napoleon-at-the-Battle-of-Wagram-1024x755.jpg",
    "https://dreamsinparis.com/wp-content/uploads/2023/05/Napoleons-Return-from-Elba-1024x766.jpg",
]

time = time.ctime()

def quote(request):
    '''Function to respond to the "quote" request.'''

    template_name = 'quotes/quote.html'
    context = {
        "quote": quotes[random.randint(1,4)-1],
        "image": images[random.randint(1,4)-1],
        "time": time,
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
