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