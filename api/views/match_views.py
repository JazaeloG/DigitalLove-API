from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Like, Match
from ..serializers.match_serializers import LikeSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from drf_spectacular.utils import extend_schema

@extend_schema(methods=['POST'], request=LikeSerializer, responses={201: LikeSerializer}, tags=['Match'], description='Dar like a un usuario')
@api_view(['POST'])
def like_user(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')
    existing_like = Like.objects.filter(sender_id=sender_id, receiver_id=receiver_id).first()
    if existing_like:
        return Response({'message': 'Ya has enviado un like a este usuario'}, status=status.HTTP_400_BAD_REQUEST)

    like_serializer = LikeSerializer(data={'sender_id': sender_id, 'receiver_id': receiver_id})
    if like_serializer.is_valid():
        like_instance = like_serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notification_%s' % receiver_id,
            {
                'type': 'send_notification',
                'notification': 'Has recibido un nuevo like de %s' % sender_id
            }
        )

        return Response({'message': 'Like enviado correctamente'}, status=status.HTTP_201_CREATED)
    else:
        return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(methods=['POST'], request=LikeSerializer, responses={200: LikeSerializer}, tags=['Match'], description='Responder a un like')
@api_view(['POST'])
def respond_to_like(request):
    receiver_id = request.data.get('receiver_id')
    sender_id = request.data.get('sender_id')
    action = request.data.get('accion')

    like_instance = Like.objects.filter(sender_id=sender_id, receiver_id=receiver_id).first()
    if not like_instance:
        return Response({'message': 'No se encontró el like'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'accept': 
        like_instance.accepted = True
        like_instance.save()
        Match.objects.create(usuario1_id=sender_id, usuario2_id=receiver_id)
        return Response({'message': 'Match aceptado'}, status=status.HTTP_200_OK)
    elif action == 'decline':
        like_instance.delete()
        return Response({'message': 'Like declinado'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Acción no válida'}, status=status.HTTP_400_BAD_REQUEST)
