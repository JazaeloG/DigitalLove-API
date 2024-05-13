from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from api.models import Usuario, Reporte
from django.utils import timezone
from datetime import datetime

from chatApp.consumers import NotificationConsumer
from ..serializers.reporte_serializer import ReporteSerializer
from api.helpers.reporte_helper import ValidacionesReporte

@extend_schema(description='Reportar usuario', responses={201: ReporteSerializer}, tags=['Reporte'], request=ReporteSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def reportar_usuario(request):
    serializer = ReporteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        report_data = serializer.data
        notification_consumer = NotificationConsumer()
        await notification_consumer.send_report_notification(report_data)

        return Response({'message': ValidacionesReporte.REPORTE_REGISTRADO.value}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(description='Ver reportes', responses={200: ReporteSerializer}, tags=['Reporte'], request=None)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_reportes(request):
    fecha_inicio = request.query_params.get('fecha_inicio', None)
    fecha_fin = request.query_params.get('fecha_fin', None)

    reportes = Reporte.objects.all()

    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            reportes = reportes.filter(fechaRegistro__range=[fecha_inicio, fecha_fin])
        except ValueError:
            return Response({'message': 'Formato de fecha incorrecto. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReporteSerializer(reportes, many=True)
    return Response(serializer.data)

@extend_schema(description='Ver reportes de un usuario', responses={200: ReporteSerializer}, tags=['Reporte'], request=None)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_reportes_usuario(request, usuario_id):
    reportes = Reporte.objects.filter(usuario_reportado_id=usuario_id)
    serializer = ReporteSerializer(reportes, many=True)
    return Response(serializer.data)