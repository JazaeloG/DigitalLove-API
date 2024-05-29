from django.db import models
from django.forms import ValidationError
from api.enums.estado_usuario import EstadoUsuario
from api.enums.orientacion_sexual import OrientacionSexual, SexoPreferido
from api.enums.sexo_usuario import SexoUsuario
from api.enums.tipo_usuario import TipoUsuario
from api.enums.estados_pais import EstadosMexico
from api.enums.motivos_reporte_ import MotivosReporte
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from api.enums.cabello_preferencias import CabelloColorPreferencias, CabelloTipoPreferencias

class CustomUserManager(BaseUserManager):
    def create_user(self, usuario, email, password, tipoUsuario=TipoUsuario.USUARIO.value, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(usuario=usuario, correo=email, tipoUsuario=tipoUsuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, email, password, **extra_fields):
        extra_fields.setdefault('tipoUsuario', TipoUsuario.ADMIN.value)
        return self.create_user(usuario, email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    tipoUsuario = models.CharField(max_length=20, choices=[( tipo.name, tipo.value)for tipo in TipoUsuario], default=TipoUsuario.USUARIO.value)
    nombre = models.CharField(max_length=50, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    apellidoMaterno = models.CharField(max_length=50, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    apellidoPaterno = models.CharField(max_length=50, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    edad = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(99)], default=18)
    ubicacion = models.CharField(max_length=50, choices=[(estado.name, estado.value) for estado in EstadosMexico], default=EstadosMexico.CIUDAD_DE_MEXICO.value)
    sexo = models.CharField(max_length=20, choices=[(sexo.name, sexo.value) for sexo in SexoUsuario], default=SexoUsuario.FEMENINO.value)
    telefono = models.CharField(max_length=15, validators=[MinLengthValidator(10), MaxLengthValidator(15)])
    usuario = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(1), MaxLengthValidator(50)])
    estado = models.CharField(max_length=20, choices=[( estado.name, estado.value) for estado in EstadoUsuario],default=EstadoUsuario.ACTIVO.value)
    correo = models.EmailField(max_length=50, validators=[EmailValidator()])
    password = models.CharField(max_length=255, blank=False, null=False)
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    orientacionSexual = models.CharField(max_length=20, choices=[(orientacion.name, orientacion.value) for orientacion in OrientacionSexual], default=OrientacionSexual.HETEROSEXUAL.value)

    USERNAME_FIELD = 'usuario'
    EMAIL_FIELD = 'correo'
    PASSWORD_FIELD = 'password'
    REQUIRED_FIELDS = ['correo', 'password']
    objects = CustomUserManager()

    def __str__(self):
        return self.nombre

class FotoUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='uploads/', blank=True, null=True, validators=[MaxValueValidator(3)])

    def save(self, *args, **kwargs):
        self.foto.name = f'{self.usuario.usuario}/{self.foto.name}'
        super().save(*args, **kwargs)
    
class Like(models.Model):
    envia = models.ForeignKey(Usuario, related_name='like_envia', on_delete=models.CASCADE, null=False)
    recibe = models.ForeignKey(Usuario, related_name='like_recibe', on_delete=models.CASCADE, null=False)
    aceptado = models.BooleanField(default=False)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('envia', 'recibe')


class Match(models.Model):
    usuario1 = models.ForeignKey(Usuario, related_name='match1', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(Usuario, related_name='match2', on_delete=models.CASCADE)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario1', 'usuario2')

    def clean(self):
        if self.usuario1 == self.usuario2:
            raise ValidationError("Un usuario no puede hacer match consigo mismo.")
        
class Reporte(models.Model):
    usuario_reportado = models.ForeignKey(Usuario, related_name='reportes_recibidos', on_delete=models.CASCADE)
    motivo = models.CharField(choices=[(motivo.name, motivo.value) for motivo in MotivosReporte], default='', max_length=100)
    comentario = models.TextField(max_length=500, null=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.usuario_reportado == self.usuario_reportado:
            raise ValidationError("Un usuario no puede reportarse a sí mismo.")
        if not self.motivo:
            raise ValidationError("El motivo del reporte no puede estar vacío.")
    
    def __str__(self):
        return self.motivo

class AtributosUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    caraOvalada = models.BooleanField(default=False)
    lentes = models.BooleanField(default=False)
    pielBlanca = models.BooleanField(default=False)
    colorCabello = models.CharField(max_length=50, default='')
    tipoCabello = models.CharField(max_length=50, default='')

    def _str_(self):
        return self.usuario.nombre
    
class PreferenciasUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    conLentes = models.BooleanField(default=False, null=False)
    conCaraOvalada = models.BooleanField(default=False, null=False)
    conPielBlanca = models.BooleanField(default=False, null=False)
    colorCabello = models.CharField(max_length=50, choices=[(cabello.name, cabello.value) for cabello in CabelloColorPreferencias], default=CabelloColorPreferencias.BLACK_HAIR.value)
    tipoCabello = models.CharField(max_length=50, choices=[(tipo.name, tipo.value) for tipo in CabelloTipoPreferencias], default=CabelloTipoPreferencias.STRAIGHT_HAIR.value)
    sexoPreferido = models.CharField(max_length=20, choices=[(sexo.name, sexo.value) for sexo in SexoPreferido], default=SexoPreferido.AMBOS.value)