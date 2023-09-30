from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=500, default='')
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='followers_profile') #repersents the users who follow the current user
    following = models.ManyToManyField(User, related_name='following_profile') #repersents the users who the current user follows




