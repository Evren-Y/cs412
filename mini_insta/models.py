# file: mini_insta/models.py
# Author: Evren Yaman (yamane@bu.edu), 10/3/2025
# Description: Models for the database.

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a personal Profile by an user of the mini_insta app'''

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        ''' Return a readable string showing the display name and bio snippet. '''
        return f'{self.bio_text} by {self.display_name}'
    
    def get_all_posts(self):
        ''' Return all Post objects associated with this Profile, ordered by most recent timestamp first. '''
        posts = Post.objects.filter(profile=self)
        return posts.order_by('-timestamp')

class Post(models.Model):
    ''' Represents a single post created by a Profile. '''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Return a readable string showing the caption and profile username. '''
        return f'{self.caption} by {self.profile.username}'

    def get_all_photos(self):
        ''' Return all Photo objects associated with this Post, ordered by most recent timestamp first. '''
        photos = Photo.objects.filter(post=self)
        return photos.order_by('-timestamp')
    
class Photo(models.Model):
    ''' Represents an image attached to a Post. '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def get_image_url(self):
        ''' Return the URL of the image. '''

        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        return None

    def __str__(self):
        ''' Return a readable string showing the image URL and username of owner. '''

        if self.image_url:
            return f'{self.image_url} by {self.post.profile.username}'
        elif self.image_file:
            return f'{self.image_file.name} by {self.post.profile.username}'
        return "No image"