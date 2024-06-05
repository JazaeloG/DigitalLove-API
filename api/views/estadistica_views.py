from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from ..models import Usuario, Reporte
from api.enums.estados_pais import EstadosMexico
from drf_spectacular.utils import extend_schema
from ..serializers import estadistica_serializers

@extend_schema(
    methods=['GET'], 
    responses={200: estadistica_serializers.EstadisticasSerializer}, 
    tags=['Estadísticas'], 
    description='Obtener estadísticas de usuarios y reportes'
)
@api_view(['GET'])
def obtener_estadisticas(request):
    try:        
        total_usuarios = Usuario.objects.count()

        usuarios_por_estado = Usuario.objects.values('ubicacion').annotate(total=Count('ubicacion')).order_by('-total')
        estado_con_mas_usuarios = usuarios_por_estado[0]['ubicacion'] if usuarios_por_estado else None
        
        usuarios_activos = Usuario.objects.filter(estado='ACTIVO').count()

        
        total_reportes = Reporte.objects.count()

        
        reportes_por_estado = (Reporte.objects
                               .values('usuario_reportado__ubicacion')
                               .annotate(total=Count('usuario_reportado__ubicacion'))
                               .order_by('-total'))
        estado_con_mas_reportes = reportes_por_estado[0]['usuario_reportado__ubicacion'] if reportes_por_estado else None

        ubicaciones = {estado.value: 0 for estado in EstadosMexico}
        for usuario in usuarios_por_estado:
            estado = usuario['ubicacion']
            total = usuario['total']
            ubicaciones[estado] = total

        data = {
            'total_usuarios': total_usuarios,
            'estado_con_mas_usuarios': estado_con_mas_usuarios,
            'usuarios_activos': usuarios_activos,
            'total_reportes': total_reportes,
            'estado_con_mas_reportes': estado_con_mas_reportes,
            'ubicaciones': ubicaciones
        }

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
