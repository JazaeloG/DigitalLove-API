from rest_framework import serializers
from api.models import Usuario
from api.serializers.usuarios_serializers import FotoUsuarioSerializer, UsuarioMinimalSerializer, UsuarioSerializer
from ..models import ChatPersonal, MensajeChat

class UsuarioChatSerializer(serializers.ModelSerializer):
    fotos = FotoUsuarioSerializer(many=True, required=False)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'edad', 'fotos']

class ChatPersonalSerializer(serializers.ModelSerializer):
    usuario = UsuarioChatSerializer(read_only=True)
    usuario_match = UsuarioChatSerializer(read_only=True)

    class Meta:
        model = ChatPersonal
        fields = ['id', 'usuario', 'usuario_match', 'fechaRegistro']

    def get_usuario(self, obj):
        request = self.context.get('request')
        usuario_id = request.parser_context['kwargs']['usuario_id']
        if obj.usuario_id == usuario_id:
            return UsuarioChatSerializer(obj.usuario, context=self.context).data
        return UsuarioMinimalSerializer(obj.usuario, context=self.context).data

    def get_usuario_match(self, obj):
        request = self.context.get('request')
        usuario_id = request.parser_context['kwargs']['usuario_id']
        if obj.usuario_match_id == usuario_id:
            return UsuarioChatSerializer(obj.usuario_match, context=self.context).data
        return UsuarioMinimalSerializer(obj.usuario_match, context=self.context).data

class MensajeChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeChat
        fields = '__all__'
