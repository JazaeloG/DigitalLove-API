from rest_framework import serializers
from api.models import Usuario, UsuarioAdministrador

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = ('user','password')
        

class UsuarioAdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioAdministrador
        exclude = ('password', 'user')
        