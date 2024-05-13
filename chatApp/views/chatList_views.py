from rest_framework import generics
from rest_framework.response import Response
from ..models import ChatPersonal, ChatGrupal
from ..serializers import chat_serializers

class userChatList(generics.ListAPIView):
    serializer_class = chat_serializers

    def get_queryset(self):
        usuario_id = self.kwargs['usuario_id']  
        
        chats_personales = ChatPersonal.objects.filter(usuario_id=usuario_id)
        chats_grupales = ChatGrupal.objects.filter(usuarios__id=usuario_id)
        
        return chats_personales | chats_grupales
