from rest_framework import serializers

class EstadisticasSerializer(serializers.Serializer):
    total_usuarios = serializers.IntegerField()
    estado_con_mas_usuarios = serializers.CharField(allow_null=True)
    usuarios_activos = serializers.IntegerField()
    total_reportes = serializers.IntegerField()
    estado_con_mas_reportes = serializers.CharField(allow_null=True)
