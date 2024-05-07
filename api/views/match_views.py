from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chatApp.serializers.notification_serializers import NotificacionSerializer
from ..models import Like, Match, Usuario
from chatApp.models import ChatPersonal
from ..serializers.match_serializers import LikeSerializer, MatchSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(methods=['POST'], request=LikeSerializer, responses={201: LikeSerializer}, tags=['Match'], description='Dar like a un usuario')
@api_view(['POST'])
def like_user(request):
    envia_id = request.data.get('envia')
    recibe_id = request.data.get('recibe')
    try:
        recibe_user = Usuario.objects.get(id=recibe_id)
        envia_user = Usuario.objects.get(id=envia_id)
    except Usuario.DoesNotExist:
        return Response({'message': 'El usuario receptor no existe'}, status=status.HTTP_400_BAD_REQUEST)
    existing_like = Like.objects.filter(recibe_id=recibe_id, envia_id=envia_id).first()
    if existing_like:
        return Response({'message': 'Ya has enviado un like a este usuario'}, status=status.HTTP_400_BAD_REQUEST)
    like_serializer = LikeSerializer(data={'envia': envia_id, 'recibe': recibe_id})
    if like_serializer.is_valid():
        like_instance = like_serializer.save()

        notification_data = {
            'usuario': recibe_id,
            'mensaje': f'{envia_user} te ha dado like!'
        }
        notification_serializer = NotificacionSerializer(data=notification_data)
        if notification_serializer.is_valid():
            notification_serializer.save()
            
        else:
            return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Like enviado correctamente'}, status=status.HTTP_201_CREATED)
    else:
        return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@extend_schema(methods=['POST'], request=MatchSerializer, responses={200: LikeSerializer}, tags=['Match'], description='Responder a un like')
@api_view(['POST'])
def respond_to_like(request):
    receiver_id = request.data.get('recibe_id')
    sender_id = request.data.get('envia_id')
    action = request.data.get('accion')

    

    like_instance = Like.objects.filter(envia_id=sender_id, recibe_id=receiver_id).first()
    if not like_instance:
        return Response({'message': 'No se encontró el like'}, status=status.HTTP_404_NOT_FOUND)

    if like_instance.aceptado:
        return Response({'message': 'El match ya fue aceptado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)
    
    if action: 
        like_instance.aceptado = True
        like_instance.save()
        Match.objects.create(usuario1_id=sender_id, usuario2_id=receiver_id)
        ChatPersonal.objects.create(usuario_id=sender_id, usuario_match_id=receiver_id)
        return Response({'message': 'Match aceptado'}, status=status.HTTP_200_OK)
    else:
        like_instance.delete()
        return Response({'message': 'Like declinado'}, status=status.HTTP_200_OK)