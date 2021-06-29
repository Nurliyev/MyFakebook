from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    bio = models.TextField(default='...', max_length=250)
    friends = models.ManyToManyField('User', blank=True, symmetrical=True, related_name='friends')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default='../static/img/default-profile.png')


class Friendships(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
