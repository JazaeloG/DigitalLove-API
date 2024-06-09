from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.enums.tipo_usuario import TipoUsuario
from api.helpers.reporte_helper import ValidacionesReporte
from api.helpers.usuario_helper import ErroresUsuario
from api.models import Reporte, Usuario
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from channels.layers import get_channel_layer
from rest_framework import status
from drf_spectacular.utils import extend_schema
from api.serializers.reporte_serializer import ReporteSerializer
from api.serializers.usuarios_serializers import UsuarioBloquearSerializer
from chatApp.models import Notificacion
from chatApp.serializers.notification_serializers import NotificacionSerializer

@extend_schema(methods=['GET'], responses={200: NotificacionSerializer}, tags=['Notificaciones'], description='Listar notificaciones de un usuario')
@api_view(['GET'])
def listar_notificaciones(request, usuario_id):
    try:
        notificaciones = Notificacion.objects.filter(usuario_recibe_id=usuario_id)
        serializer = NotificacionSerializer(notificaciones, many=True)
        return Response(serializer.data)
    except Notificacion.DoesNotExist:
        return Response({'message': ErroresUsuario.NOTIFICACIONES_NO_ENCONTRADAS.value}, status=status.HTTP_404_NOT_FOUND)
    
@extend_schema(methods=['POST'], responses={200: NotificacionSerializer}, tags=['Notificaciones'], description='Enviar notificación a un usuario', request=NotificacionSerializer)
@api_view(['POST'])
def enviar_notificacion(request):
    envia_id = request.data.get('usuario_envia_id')
    user_id = request.data.get('usuario_recibe_id')
    try:
        usuario_envia = Usuario.objects.get(id=envia_id)
        usuario_recibe = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': ErroresUsuario.USUARIO_NO_REGISTRADO.value}, status=400)

    notification_message = request.data.get('mensaje')
    if not notification_message:
        return JsonResponse({'success': False, 'error': ErroresUsuario.NO_MENSAJE_NOTIFICACION.value}, status=400)

    try:
        Notificacion.objects.create(
            usuario_envia_id=usuario_envia,
            usuario_recibe_id=usuario_recibe,
            mensaje=notification_message
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user_id}',
            {
                'type': 'notification_message',
                'message': notification_message
            }
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
@extend_schema(
    request=NotificacionSerializer,
    methods=['POST'],
    responses={200: NotificacionSerializer},
    tags=['Notificaciones'],
    description='Enviar notificación de reporte a todos los administradores'
)
@api_view(['POST'])
def send_report_to_admin(request):
    try:
        reporte_data = request.data.get('reporte')
        if not reporte_data:
            return JsonResponse({'success': False, 'error': ValidacionesReporte.REPORTE_OBLIGATORIO.value}, status=status.HTTP_400_BAD_REQUEST)


        administradores = Usuario.objects.filter(tipoUsuario=TipoUsuario.ADMIN.value)
        if not administradores.exists():
            return JsonResponse({'success': False, 'error': ValidacionesReporte.NO_ADMINISTRADORES.value}, status=status.HTTP_404_NOT_FOUND)

        channel_layer = get_channel_layer()
        
        for admin in administradores:
            async_to_sync(channel_layer.group_send)(
                f'notifications_{admin.id}',
                {
                    'type': 'send_report_notification',
                    'report': reporte_data
                }
            )
        
        return JsonResponse({'success': True}, status=status.HTTP_200_OK)
    
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': ErroresUsuario.USUARIO_NO_REGISTRADO.value}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@extend_schema(
    methods=['GET'],
    tags=['Reporte'],
    description="Recuperacion de anteriores reportes",
    responses={200: ReporteSerializer}  
)
@api_view(['GET'])
def recuperar_reportes(request):
    reportes = Reporte.objects.all().order_by('-fechaRegistro')
    serializer = ReporteSerializer(reportes, many=True)
    return JsonResponse(serializer.data, safe=False)
