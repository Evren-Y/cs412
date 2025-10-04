# file: mini_insta/urls.py
# Author: Evren Yaman (yamane@bu.edu), 9/26/2025
# Description: extension of cs412 urls.py file, creating the paths for all pages used in the mini_insta web application.

from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
]