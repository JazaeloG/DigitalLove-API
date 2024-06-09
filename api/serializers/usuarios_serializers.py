from rest_framework import serializers
from api.enums.etiquetas_usuario import Etiquetas
from api.models import FotoUsuario, PreferenciasUsuario, Usuario

class FotoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoUsuario
        fields = ['id', 'foto']

class UsuarioSerializer(serializers.ModelSerializer):
    fotos = FotoUsuarioSerializer(many=True, required=False)

    class Meta:
        model = Usuario
        fields = ['id', 'usuario', 'nombre', 'apellidoMaterno', 'apellidoPaterno', 'edad', 'ubicacion', 'sexo', 'telefono', 'estado', 'correo','orientacionSexual', 'password', 'fechaRegistro', 'fotos']

    def create(self, validated_data):
        fotos_data = validated_data.pop('fotos', [])
        usuario = Usuario.objects.create(**validated_data)
        for foto_data in fotos_data:
            FotoUsuario.objects.create(usuario=usuario, **foto_data)
        return usuario

    def update(self, instance, validated_data):
        fotos_data = validated_data.pop('fotos', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for foto_data in fotos_data:
            if 'id' in foto_data:
                foto_id = foto_data.pop('id')
                foto = FotoUsuario.objects.get(id=foto_id, usuario=instance)
                foto.foto = foto_data.get('foto', foto.foto)
                foto.save()
            else:
                FotoUsuario.objects.create(usuario=instance, **foto_data)
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        fotos = FotoUsuario.objects.filter(usuario=instance)
        representation['fotos'] = FotoUsuarioSerializer(fotos, many=True).data
        return representation
    
class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128)

class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','usuario', 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'correo', 'fechaRegistro', 'password']

class UsuarioBloquearSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()

class PreferenciasUsuarioSerializer(serializers.ModelSerializer):
    etiquetas = serializers.ListField(
        child=serializers.ChoiceField(choices=[etiqueta.value for etiqueta in Etiquetas]),
        max_length=6,
        allow_empty=True
    )
    
    class Meta:
        model = PreferenciasUsuario
        exclude = ['usuario']

    def update(self, instance, validated_data):
        etiquetas = validated_data.pop('etiquetas', None) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        
        if etiquetas is not None:
            instance.etiquetas = etiquetas
            instance.save()
        return instance

    def validate_etiquetas(self, value):
        if len(value) > 6:
            raise serializers.ValidationError("No puedes seleccionar más de 6 etiquetas.")
        return value

class EliminarFotoSerializer(serializers.Serializer):
    pass

class AgregarFotoSerializer(serializers.Serializer):
    foto = serializers.ImageField()

    def validate_foto(self, value):
        if value is None:
            raise serializers.ValidationError("La foto no puede estar vacía.")
        return value
    
class UsuarioMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id']