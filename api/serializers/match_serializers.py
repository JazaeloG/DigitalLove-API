from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from ..models import FotoUsuario, Like, Usuario

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['envia', 'recibe']

class MatchSerializer(serializers.Serializer):
    envia_id = serializers.IntegerField()
    recibe_id = serializers.IntegerField()
    accion = serializers.BooleanField()

class UsuarioMatchSerializer(serializers.ModelSerializer):
    fotos = serializers.SerializerMethodField()
    puntuacion = serializers.IntegerField(default=0)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellidoPaterno','ubicacion', 'correo', 'fotos','edad','sexo','puntuacion']

    @extend_schema_field(serializers.ListField(child=serializers.URLField()))
    def get_fotos(self, obj):
        fotos = FotoUsuario.objects.filter(usuario=obj)
        return [foto.foto.url for foto in fotos]