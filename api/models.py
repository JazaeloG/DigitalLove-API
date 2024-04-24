from django.db import models
from api.enums.tipo_usuario import TipoUsuario

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, default=TipoUsuario.USUARIO.value)
    nombre = models.CharField(max_length=50)
    apellidoMaterno = models.CharField(max_length=50)
    apellidoPaterno = models.CharField(max_length=50)
    edad = models.IntegerField()
    genero = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    correo = models.EmailField(max_length=50)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class UsuarioAdministrador(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, default=TipoUsuario.ADMIN.value)
    nombre = models.CharField(max_length=50)
    apellidoMaterno = models.CharField(max_length=50)
    apellidoPaterno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    correo = models.EmailField(max_length=50)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
