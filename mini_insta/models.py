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
        return f'{self.bio_text} by {self.display_name}'
    
    def get_all_posts(self):
        ''' '''
        posts = Post.objects.filter(profile=self)
        return posts.order_by('-timestamp')

class Post(models.Model):
    ''' '''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.caption} by {self.profile.username}'

    def get_all_photos(self):
        ''' '''
        photos = Photo.objects.filter(post=self)
        return photos.order_by('-timestamp')
    
class Photo(models.Model):
    ''' '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.image_url} by {self.post.profile.username}'