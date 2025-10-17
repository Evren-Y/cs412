# file: mini_insta/models.py
# Author: Evren Yaman (yamane@bu.edu), 10/3/2025
# Description: Models for the database.

from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        """Return the URL for this Profile’s detail page."""
        return reverse('profile', args=[str(self.pk)])
    
    def get_followers(self):
        '''Return a Python list of Profile objects that follow THIS profile. '''

        qs = Follow.objects.filter(profile=self).select_related('follower_profile')
        return [f.follower_profile for f in qs]

    def get_num_followers(self):
        ''' Return the count of followers (int). '''

        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        '''Return a Python list of Profile objects that THIS profile follows. '''

        qs = Follow.objects.filter(follower_profile=self).select_related('profile')
        return [f.profile for f in qs]

    def get_num_following(self):
        ''' Return the count of profiles this profile is following (int). '''

        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        ''' Return a QuerySet of Posts made by Profiles that this Profile follows,
        ordered from newest to oldest. '''
        
        # Get all the Follow objects where this profile is the follower
        following_rels = Follow.objects.filter(follower_profile=self)

        # Extract the followed Profile objects (publishers)
        followed_profiles = [f.profile for f in following_rels]

        # If not following anyone, return an empty QuerySet
        if not followed_profiles:
            return Post.objects.none()

        # Retrieve posts from those profiles
        feed_posts = Post.objects.filter(profile__in=followed_profiles).order_by('-timestamp')

        return feed_posts


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
    
    def get_all_comments(self):
        ''' Return all Comment objects for this Post, newest first. '''
        return Comment.objects.filter(post=self).select_related('profile').order_by('-timestamp')
    
    def get_likes(self):
        ''' Return all Like objects for this Post. '''
        return Like.objects.filter(post=self).select_related('profile').order_by('-timestamp')

    def get_num_likes(self):
        ''' Return the number of likes on this Post. '''
        return Like.objects.filter(post=self).count()

    
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
    
class Follow(models.Model):
    ''' Represents a "follow" edge, follower_profile linked to another profile. '''

    # The profile being followed
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    # The profile that follows
    follower_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="follower_profile"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'follower_profile')

    def __str__(self):
        ''' String representation '''
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'
    

class Comment(models.Model):
    ''' A comment that one Profile makes on a Post. '''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f'{self.profile.display_name } on Post {self.post_id}: {self.text[:40]}{"…" if len(self.text) > 40 else ""}'
    
class Like(models.Model):
    ''' One Profile 'liking' a Post. '''

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'profile')

    def __str__(self):
        return f'{self.profile.display_name} liked Post {self.post_id}'

