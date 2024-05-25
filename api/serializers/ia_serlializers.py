from rest_framework import serializers

class AtributosSerializer(serializers.Serializer):
    file = serializers.ImageField()

class CompararRostrosSerializer(serializers.Serializer):
    imagenRostro = serializers.ImageField()
    imagenIdentificacion = serializers.ImageField()