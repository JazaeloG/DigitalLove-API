from django.db import models
from django.conf import settings

# Create your models here.
class ChatPersonal(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_usuario')
    usuario_match = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_usuario_match')
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'usuario_match']

    def __str__(self):
        return f'{self.usuario} - {self.usuario_match}'
    
class ChatGrupal(models.Model):
    nombre = models.CharField(max_length=50)
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos')
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.nombre
    
class MensajeGrupal(models.Model):
    chat = models.ForeignKey(ChatGrupal, on_delete=models.CASCADE, related_name='mensajesChat')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuario_mensajes')
    mensaje = models.TextField()
    fechaEnvio = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.chat} - {self.usuario} - {self.mensaje}'

class MensajeChatPersonal(models.Model):
    chat_personal = models.ForeignKey(ChatPersonal, on_delete=models.CASCADE, related_name='mensajes')
    sender_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    recipient_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.sender_id} para {self.recipient_id} en {self.chat_personal}'
    
class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fechaEnvio = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.usuario} - {self.mensaje}'

