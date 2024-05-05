from django.db import models
from django.forms import ValidationError
from api.enums.estado_usuario import EstadoUsuario
from api.enums.sexo_usuario import SexoUsuario
from api.enums.tipo_usuario import TipoUsuario
from api.enums.estados_pais import EstadosMexico
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None,tipo_usuario=TipoUsuario.USUARIO.value, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, tipoUsuario=tipo_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('tipoUsuario', TipoUsuario.ADMIN.value)
        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    tipoUsuario = models.CharField(max_length=20, default=TipoUsuario.USUARIO.value, editable=False)
    nombre = models.CharField(max_length=50, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    apellidoMaterno = models.CharField(max_length=50, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    apellidoPaterno = models.CharField(max_length=50, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    edad = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    ubicacion = models.CharField(max_length=50, choices=[(estado.name, estado.value) for estado in EstadosMexico], default=EstadosMexico.CIUDAD_DE_MEXICO.value)
    sexo = models.CharField(max_length=20, choices=[(sexo.name, sexo.value) for sexo in SexoUsuario], default=SexoUsuario.FEMENINO.value)
    telefono = models.CharField(max_length=15, unique=True, validators=[MinLengthValidator(10), MaxLengthValidator(15)])
    usuario = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    estado = models.CharField(max_length=20, default=EstadoUsuario.ACTIVO.value, editable=False)
    correo = models.EmailField(max_length=50, unique=True, validators=[EmailValidator()])
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    fotos = models.ImageField(upload_to='fotos/', blank=True)

    USERNAME_FIELD = 'usuario'
    EMAIL_FIELD = 'correo'
    REQUIRED_FIELDS = ['correo']
    objects = CustomUserManager()

    def __str__(self):
        return self.nombre
    
class Like(models.Model):
    sender = models.ForeignKey(Usuario, related_name='likes_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Usuario, related_name='likes_received', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')


class Match(models.Model):
    usuario1 = models.ForeignKey(Usuario, related_name='matches1', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(Usuario, related_name='matches2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario1', 'usuario2')

    def clean(self):
        if self.usuario1 == self.usuario2:
            raise ValidationError("Un usuario no puede hacer match consigo mismo.")