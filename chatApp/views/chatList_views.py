from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.helpers.match_helper import ErrorLike
from ..models import ChatPersonal, MensajeChat
from ..serializers import chat_serializers
from drf_spectacular.utils import extend_schema
from rest_framework import status


@extend_schema(methods=['GET'], responses={200: chat_serializers.ChatPersonalSerializer(many=True)}, tags=['Chat'], description='Obtener los chats de un usuario')
@api_view(['GET'])
def get_user_chats(request, usuario_id):
    try:
        chats_usuario = ChatPersonal.objects.filter(usuario_id=usuario_id)
        chats_usuario_match = ChatPersonal.objects.filter(usuario_match_id=usuario_id)
        chats_personales = chats_usuario | chats_usuario_match
        serializer = chat_serializers.ChatPersonalSerializer(chats_personales, many=True)
        return Response({"chats": serializer.data})
    except ChatPersonal.DoesNotExist:
        return Response({'message': ErrorLike.NO_CHATS_PERSONALES.value}, status=status.HTTP_404_NOT_FOUND)
    
@extend_schema(methods=['GET'], responses={200: chat_serializers.MensajeChatSerializer(many=True)}, tags=['Chat'], description='Obtener los mensajes de un chat')
@api_view(['GET'])
def obtener_mensajes_anteriores(request, chat_personal_id):
    try:
        mensajes = MensajeChat.objects.filter(chat_id=chat_personal_id).order_by('fechaRegistro')
        seriallizer = chat_serializers.MensajeChatSerializer(mensajes, many=True)
        return Response({'mensajes': seriallizer.data})
    except MensajeChat.DoesNotExist:
        return Response({'error': ErrorLike.NO_MENSAJES_CHAT.value}, status=404)