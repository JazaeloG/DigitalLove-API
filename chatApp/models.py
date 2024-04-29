from django.db import models
from django.contrib.auth.models import User

# Estos son los modelos de chat para la aplicación de chat.
class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)