from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.
class Chat(models.Model):
    def by_user(self, **kwargs):
        usuario = kwargs.get('usuario')
        lookup = Q(usuario=usuario) | Q(usuario_match=usuario)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs

class ChatPersonal(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='primer_usuario_chat')
    usuario_match = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='segundo_usuario_chat')
    actualizado = models.DateTimeField(auto_now=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    objects = Chat()
    class Meta:
        unique_together = ['usuario', 'usuario_match']

class MensajeChat(models.Model):
    chat = models.ForeignKey(ChatPersonal, on_delete=models.CASCADE, related_name='mensajes_chat')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fechaRegistro = models.DateTimeField(auto_now_add=True)

class Notificacion(models.Model):
    usuario_envia_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones_enviadas')
    usuario_recibe_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones_recibidas')
    mensaje = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)