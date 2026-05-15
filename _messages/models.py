from django.db import models
from django.conf import settings


class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ConvUser", related_name="conversations")
    updated_at = models.DateTimeField(auto_now=True)
    
class ConvUser(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unread_count = models.IntegerField(default=0)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ("conversation", "user")
        
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to="chat_images/",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)