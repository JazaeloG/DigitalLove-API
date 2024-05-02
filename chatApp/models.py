from django.db import models
from api.models import Usuario

class Chat(models.Model):
    usuarios = models.ManyToManyField(Usuario, related_name='chats')

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)