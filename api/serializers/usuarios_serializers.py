from rest_framework import serializers
from api.models import PreferenciasUsuario, Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'usuario', 'nombre', 'apellidoMaterno', 'apellidoPaterno', 'edad', 'ubicacion', 'sexo', 'telefono', 'estado', 'correo', 'password', 'fechaRegistro', 'fotos']

class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128)

class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','usuario', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'correo', 'fechaRegistro', 'password']

class UsuarioBloquearSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()

class PreferenciasUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciasUsuario
        exclude = ['usuario']