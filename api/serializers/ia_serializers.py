from rest_framework import serializers

class AtributosSerializer(serializers.Serializer):
    file = serializers.FileField()

class CompararRostrosSerializer(serializers.Serializer):
    imagenRostro = serializers.FileField()
    imagenIdentificacion = serializers.FileField()