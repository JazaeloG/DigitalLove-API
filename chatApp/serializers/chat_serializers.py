from rest_framework import serializers
from ..models import ChatPersonal, MensajeChat

class ChatPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatPersonal
        fields = ['id', 'usuario', 'usuario_match', 'fechaRegistro']

class MensajeChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeChat
        fields = '__all__'

