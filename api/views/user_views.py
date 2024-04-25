from rest_framework import viewsets, status
from ..serializers.usuarios_serializers import  UsuarioSerializer, UsuarioAdministradorSerializer
from api.models import Usuario, UsuarioAdministrador
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioAdministradorViewSet(viewsets.ModelViewSet):
    queryset = UsuarioAdministrador.objects.all()
    serializer_class = UsuarioAdministradorSerializer

@api_view(['POST'])
def registrarUsuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data['password']
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        usuario = serializer.save()
        user_instance = User.objects.create(username=usuario.usuario, email=usuario.correo)
        usuario.user = user_instance
        usuario.save()
        token, created = Token.objects.get_or_create(user=user_instance)
        return Response({'status_code': status.HTTP_201_CREATED, 'message': "Usuario Creado"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginUsuario(request):
    usuario = get_object_or_404(Usuario, usuario=request.data['usuario'])
    password = request.data['password']
    if check_password(password, usuario.password):
        token, created = Token.objects.get_or_create(user=usuario.user)

        usuario_serializer = UsuarioSerializer(usuario)
        return Response({'token': token.key, 'usuario': usuario_serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def registrarAdmin(request):
    serializer = UsuarioAdministradorSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data['password']
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        usuario = serializer.save()
        user_instance = User.objects.create(username=usuario.usuario, email=usuario.correo)
        usuario.user = user_instance
        usuario.save()
        token, created = Token.objects.get_or_create(user=user_instance)
        return Response({'status_code': status.HTTP_201_CREATED, 'message': "Usuario Creado"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginAdministrador(request):
    usuario = get_object_or_404(UsuarioAdministrador, usuario=request.data['usuario'])
    password = request.data['password']
    if check_password(password, usuario.password):
        token, created = Token.objects.get_or_create(user=usuario.user)

        usuario_serializer = UsuarioAdministradorSerializer(usuario)
        return Response({'token': token.key, 'usuario': usuario_serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)