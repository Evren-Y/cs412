# file: mini_insta/views.py
# Author: Evren Yaman (yamane@bu.edu), 9/26/2025
# Description: Class-based views for listing all Profile records and showing a single Profile detail page.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
# from .forms import CreateProfileForm
# Create your views here.

class ProfileListView(ListView):
    ''' Display a list of all Profiles in the database '''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    ''' Display a single Profile from the database '''
    
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    ''' Display a single Post from the database '''
    
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

#class CreateProfileView(CreateView):
#    ''' '''

#    form_class = CreateProfileForm
#    template_name = "mini_insta/create_profile_form.html"