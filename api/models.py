from django.db import models
from api.enums.estado_usuario import EstadoUsuario
from api.enums.tipo_usuario import TipoUsuario
from django.contrib.auth.models import User
from api.enums.estados_pais import EstadosMexico
from api.enums.etiquetas_usuario import Etiquetas

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    tipoUsuario = models.CharField(max_length=20, default=TipoUsuario.USUARIO.value, editable=False)
    nombre = models.CharField(max_length=50)
    apellidoMaterno = models.CharField(max_length=50)
    apellidoPaterno = models.CharField(max_length=50)
    edad = models.IntegerField()
    ubicacion = models.CharField(max_length=50, choices=[(estado.name, estado.value) for estado in EstadosMexico], default=EstadosMexico.CIUDAD_DE_MEXICO.value)
    genero = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, unique=True)
    usuario = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, default=EstadoUsuario.ACTIVO.value, editable=False)
    correo = models.EmailField(max_length=50, unique=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, editable=False)

    def __str__(self):
        return self.nombre
    
class UsuarioAdministrador(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, default=TipoUsuario.ADMIN.value, editable=False)
    nombre = models.CharField(max_length=50)
    apellidoMaterno = models.CharField(max_length=50)
    apellidoPaterno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, unique=True)
    usuario = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    correo = models.EmailField(max_length=50, unique=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, editable=False)

    def __str__(self):
        return self.nombre