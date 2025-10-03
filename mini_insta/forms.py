from django import forms
from .models import Profile

class CreateProfileForm(forms.ModelForm):
    ''' '''

    class Meta:
        '''associate this form witha model from our database'''
        model = Profile
        fields = ['author', 'title']