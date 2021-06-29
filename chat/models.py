from django.db import models
from profiles.models import User


class Conversation(models.Model):
    UserOne = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserOne')
    UserTwo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserTwo')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.UserOne}-{self.UserTwo}"


class Message(models.Model):
    WhichConversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='Messages', null=True)
    SenderUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='SenderUser', null=True)
    message_text = models.TextField(max_length=500, null=True, blank=True)
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)
