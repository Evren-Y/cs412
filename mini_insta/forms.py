# file: mini_insta/forms.py
# Author: Evren Yaman (yamane@bu.edu), 10/3/2025
# Description: Form for creating a new post.

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    ''' '''

    image_url = forms.URLField(
        required=False,
        label="Image URL"
    )

    class Meta:
        '''associate this form with a model from our database'''
        model = Post
        fields = ['caption']
        widgets = {
            "caption": forms.Textarea(attrs={"rows": 3, "placeholder": "Write Here"}),
        }
        labels = {
            "caption": "Caption",
        }