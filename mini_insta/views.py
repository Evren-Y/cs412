# file: mini_insta/views.py
# Author: Evren Yaman (yamane@bu.edu), 9/26/2025
# Description: Class-based views for listing all Profile records and showing a single Profile detail page.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import CreatePostForm, UpdateProfileForm
from django.urls import reverse
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

class CreatePostView(CreateView):
    ''' A view for creating a new Post associated with a given Profile. '''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the profile from the URL pk
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # add profile into context so template can use {{ profile }}
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        # look up the Profile by pk from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # attach the Profile to the Post BEFORE saving to avoid NOT NULL error
        form.instance.profile = profile

        # save the Post
        response = super().form_valid(form)

        # also create a Photo for this post if an image_url was submitted
        # image_url = self.request.POST.get('image_url')
        #if image_url:
        #    Photo.objects.create(post=self.object, image_url=image_url)
        uploaded_files = self.request.FILES.getlist('image_files')
        
        for file in uploaded_files:
            Photo.objects.create(post=self.object, image_file=file)

        return response
    
    #redirect after submitting the form
    def get_success_url(self):
        from django.urls import reverse
        return reverse('post', args=[self.object.pk])

class UpdateProfileView(UpdateView):
    ''' A view to render a form which will update the current Profile. '''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

class DeletePostView(DeleteView):
    ''' A view for deleting Posts made by a Profile. '''

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        ''' Provides the Post being deleted and the profile associated as context. '''
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context
    
    def get_success_url(self):
        ''' Redirect to the Profile page of the Post you just deleted. '''
        return reverse('profile', args=[str(self.object.profile.pk)])

class UpdatePostView(UpdateView):
    ''' Update a Post's caption and redirect back to the post detail page. '''

    model = Post
    fields = ['caption']
    template_name = "mini_insta/update_post_form.html"
    context = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        return reverse('post', args=[str(self.object.pk)])
    
class ShowFollowersDetailView(DetailView):
    ''' Detail view for a Profile that shows who follows this profile. '''

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    ''' Detail view for a Profile that shows who this profile is following. '''

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"
