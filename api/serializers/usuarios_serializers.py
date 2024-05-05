from rest_framework import serializers
from api.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = ('password','last_login')

class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128)