from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from ..models import FotoUsuario, Like, PreferenciasUsuario, Usuario

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
    etiquetas = serializers.SerializerMethodField()
    puntuacion = serializers.IntegerField(default=0)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellidoPaterno','ubicacion', 'correo', 'fotos','edad','sexo','puntuacion', 'etiquetas']

    @extend_schema_field(serializers.ListField(child=serializers.URLField()))
    def get_fotos(self, obj):
        fotos = FotoUsuario.objects.filter(usuario=obj)
        return [foto.foto.url for foto in fotos]
    
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_etiquetas(self, obj):
        try:
            preferencias = PreferenciasUsuario.objects.get(usuario=obj)
            return preferencias.etiquetas if preferencias.etiquetas else []
        except PreferenciasUsuario.DoesNotExist:
            return []