from django.db import models
from profiles.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="liked_by", blank=True)
    avatar = models.ImageField(blank=True, upload_to='post-images')

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.content


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
