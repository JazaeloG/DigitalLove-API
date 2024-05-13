from rest_framework import serializers
from ..models import ChatPersonal, ChatGrupal

class ChatPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatPersonal
        fields = ['id', 'usuario', 'usuario_match', 'fechaRegistro']

class ChatGrupalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGrupal
        fields = ['id', 'nombre', 'usuarios', 'fechaRegistro']

class ChatSerializer(serializers.Serializer):
    chat_personal = ChatPersonalSerializer(many=True)
    chat_grupal = ChatGrupalSerializer(many=True)
