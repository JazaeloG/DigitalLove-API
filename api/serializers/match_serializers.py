from rest_framework import serializers
from ..models import Like, Usuario

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['envia', 'recibe']

class MatchSerializer(serializers.Serializer):
    envia_id = serializers.IntegerField()
    recibe_id = serializers.IntegerField()
    accion = serializers.BooleanField()

class UsuarioMatchSerializer(serializers.ModelSerializer):
    puntuacion = serializers.IntegerField(default=0)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'ubicacion', 'correo', 'fotos', 'puntuacion']