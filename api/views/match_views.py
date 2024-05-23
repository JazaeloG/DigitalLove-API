from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.helpers.match_helper import ErrorLike, ExitoLike
from ..models import Like, Match, Usuario
from chatApp.models import ChatPersonal
from ..serializers.match_serializers import LikeSerializer, MatchSerializer
from drf_spectacular.utils import extend_schema

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@extend_schema(methods=['POST'], request=LikeSerializer, responses={201: LikeSerializer}, tags=['Match'], description='Dar like a un usuario')
@api_view(['POST'])
def like_user(request):
    envia_id = request.data.get('envia')
    recibe_id = request.data.get('recibe')
    try:
        recibe_user = Usuario.objects.get(id=recibe_id)
        envia_user = Usuario.objects.get(id=envia_id)
    except Usuario.DoesNotExist:
        return Response({'message': ErrorLike.USUARIO_NO_EXISTE.value}, status=status.HTTP_400_BAD_REQUEST)

    existing_like = Like.objects.filter(recibe_id=recibe_id, envia_id=envia_id).first()
    if existing_like:
        return Response({'message': ErrorLike.LIKE_YA_ENVIADO.value}, status=status.HTTP_400_BAD_REQUEST)

    like_serializer = LikeSerializer(data={'envia': envia_id, 'recibe': recibe_id})
    if like_serializer.is_valid():
        like_instance = like_serializer.save()

        notification_data = {
            'usuario_envia_id': envia_id,
            'usuario_recibe_id': recibe_id,
            'mensaje': f'{envia_user.usuario} te ha dado like!'
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{recibe_id}',
            {
                'type': 'notification_message',
                'message': notification_data['mensaje']
            }
        )

        return Response({'message': ExitoLike.LIKE_ENVIADO.value}, status=status.HTTP_201_CREATED)
    else:
        return Response(like_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(methods=['POST'], request=MatchSerializer, responses={200: LikeSerializer}, tags=['Match'], description='Responder a un like')
@api_view(['POST'])
def respond_to_like(request):
    receiver_id = request.data.get('recibe_id')
    sender_id = request.data.get('envia_id')
    action = request.data.get('accion')

    try:
        receiver_user = Usuario.objects.get(id=receiver_id)
        sender_user = Usuario.objects.get(id=sender_id)
    except Usuario.DoesNotExist:
        return Response({'message': ErrorLike.USUARIO_NO_EXISTE.value}, status=status.HTTP_400_BAD_REQUEST)

    like_instance = Like.objects.filter(envia_id=sender_id, recibe_id=receiver_id).first()
    if not like_instance:
        return Response({'message': ErrorLike.LIKE_NO_ENCONTRADO.value}, status=status.HTTP_404_NOT_FOUND)

    if like_instance.aceptado:
        return Response({'message': ErrorLike.MATCH_YA_ACEPTADO.value}, status=status.HTTP_400_BAD_REQUEST)
    
    channel_layer = get_channel_layer()

    if action: 
        like_instance.aceptado = True
        like_instance.save()
        Match.objects.create(usuario1_id=receiver_id, usuario2_id=sender_id)
        ChatPersonal.objects.create(usuario_id=receiver_id, usuario_match_id=sender_id)

        notification_data = {
            'usuario_envia_id': receiver_id,
            'usuario_recibe_id': sender_id,
            'mensaje': f'{receiver_user.usuario} ha aceptado tu like!'
        }

        async_to_sync(channel_layer.group_send)(
            f'notifications_{sender_id}',
            {
                'type': 'notification_message',
                'message': notification_data['mensaje']
            }
        )

        return Response({'message': ExitoLike.MATCH_ACEPTADO.value}, status=status.HTTP_200_OK)
    else:
        like_instance.delete()

        notification_data = {
            'usuario_envia_id': receiver_id,
            'usuario_recibe_id': sender_id,
            'mensaje': f'{receiver_user.usuario} ha rechazado tu like.'
        }

        async_to_sync(channel_layer.group_send)(
            f'notifications_{sender_id}',
            {
                'type': 'notification_message',
                'message': notification_data['mensaje']
            }
        )

        return Response({'message': ErrorLike.LIKE_DECLINADO.value}, status=status.HTTP_200_OK)