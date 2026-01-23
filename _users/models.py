from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=150, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return static('images/avatar.svg')
    
    @property
    def website_link(self):
        if self.website and not self.website.startswith(('http://', 'https://')):
            return f'http://{self.website}'
        return self.website