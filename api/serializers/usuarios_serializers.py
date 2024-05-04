from rest_framework import serializers
from api.models import Usuario, UsuarioAdministrador

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = ('password','last_login')

class UsuarioAdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioAdministrador
        exclude = ('password','last_login')
        