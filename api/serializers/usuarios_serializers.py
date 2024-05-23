from rest_framework import serializers
from api.models import Usuario

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