from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.enums.tipo_usuario import TipoUsuario
from api.models import Usuario
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from channels.layers import get_channel_layer
from rest_framework import status
from drf_spectacular.utils import extend_schema

from chatApp.models import Notificacion
from chatApp.serializers.notification_serializers import NotificacionSerializer

@extend_schema(methods=['GET'], responses={200: NotificacionSerializer}, tags=['Notificaciones'], description='Listar notificaciones de un usuario')
@api_view(['GET'])
def listar_notificaciones(request, usuario_id):
    try:
        notificaciones = Notificacion.objects.filter(usuario_id=usuario_id)
        serializer = NotificacionSerializer(notificaciones, many=True)
        return Response(serializer.data)
    except Notificacion.DoesNotExist:
        return Response({'message': 'No se encontraron notificaciones para este usuario'}, status=status.HTTP_404_NOT_FOUND)
    
@extend_schema(methods=['POST'], responses={200: NotificacionSerializer}, tags=['Notificaciones'], description='Enviar notificación a un usuario')
@api_view(['POST'])
def enviar_notificacion(request, user_id):
    try:
        user = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El usuario especificado no existe'}, status=400)

    notification_message = request.data.get('notification')

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            'type': 'send_notification',
            'notification': notification_message
        }
    )

    return JsonResponse({'success': True})

@extend_schema(methods=['POST'], responses={200: NotificacionSerializer}, tags=['Notificaciones'], description='Enviar notificación de reporte a todos los administradores')
@api_view(['POST'])
def send_report_to_admin(request):
    administradores = Usuario.objects.filter(tipoUsuario=TipoUsuario.ADMIN.value)
    
    reporte_data = request.data.get('reporte')

    channel_layer = get_channel_layer()
    
    for admin in administradores:
        async_to_sync(channel_layer.group_send)(
            f'notifications_{admin.id}',
            {
                'type': 'send_report_notification',
                'report': reporte_data
            }
        )
    
    return JsonResponse({'success': True})

