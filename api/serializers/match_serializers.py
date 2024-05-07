from rest_framework import serializers
from ..models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['envia', 'recibe']

class MatchSerializer(serializers.Serializer):
    envia_id = serializers.IntegerField()
    recibe_id = serializers.IntegerField()
    accion = serializers.BooleanField()