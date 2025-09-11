# file: quotes/views.py
# Author: Evren Yaman (yamane@bu.edu), 9/11/2025
# Description: This file creates requests for all three pages in the quotes/urls.py file, and it renders the pages with the necessary context.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.

# python string list of Napoleon Quotes
quotes = [
    "Never interrupt your enemy when he is making a mistake.",
    "I start out by believing the worst.",
    "There are only two forces that unite men - fear and interest.",
    "The best way to keep one's word is not to give it.",
]

# python string list of Napoleon image urls
images = [
    "https://dreamsinparis.com/wp-content/uploads/2022/08/Painting-of-Napoleon-873x1024.jpg",
    "https://dreamsinparis.com/wp-content/uploads/2023/05/Napoleons-retreat-from-moscow-1024x780.jpg",
    "https://dreamsinparis.com/wp-content/uploads/2023/05/Napoleon-at-the-Battle-of-Wagram-1024x755.jpg",
    "https://dreamsinparis.com/wp-content/uploads/2023/05/Napoleons-Return-from-Elba-1024x766.jpg",
]

# Gets the current time
time = time.ctime()

def home(request):
    '''Function to respond to the "home" request. Passes in a random quote string and image url string
    to render from the html template page. Passes the time so that the footer in the base html file can work on every page.
    Functionally the same as the quote page.
    '''

    template_name = 'quotes/quote.html'
    
    # a rendered parameter that holds a random item from both the quotes and images python lists generated randomly
    # passes time for the footer html
    context = {
        "quote": quotes[random.randint(1,4)-1],
        "image": images[random.randint(1,4)-1],
        "time": time,
    }

    return render(request, template_name, context)

def quote(request):
    '''Function to respond to the "quote" request. Passes in a random quote string and image url string
    to render from the html template page. Passes the time so that the footer in the base html file can work on every page.
    '''

    template_name = 'quotes/quote.html'
    
    # a rendered parameter that holds a random item from both the quotes and images python lists generated randomly
    # passes time for the footer html
    context = {
        "quote": quotes[random.randint(1,4)-1],
        "image": images[random.randint(1,4)-1],
        "time": time,
    }

    return render(request, template_name, context)

def show_all(request):
    '''Function to respond to the "show_all" request. Passes in both the python lists(quotes and images)
    to render from the html template page. Passes the time so that the footer in the base html file can work on every page.
    '''

    template_name = 'quotes/show_all.html'

    # a rendered parameter that holds both the quotes and images python lists; passes time for the footer html
    context = {
        "quotes": quotes,
        "images": images,
        "time": time,
    }

    return render(request, template_name, context)

def about(request):
    '''Function to respond to the "about" request. Passes the time so that the footer in the base html file can work on every page.'''

    template_name = 'quotes/about.html'

    # passes the time variable for the footer html
    context = {
        "time": time,
    }

    return render(request, template_name, context)
