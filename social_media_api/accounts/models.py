from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage

# A Custom User Model that extends from the AbstractUser class
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', storage=default_storage, editable=True, blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    
    def __str__(self):
        return self.username