from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from api.enums.tipo_usuario import TipoUsuario
from api.helpers.login_helper import ErroresLogin, ExitoLogin
from api.helpers.registro_helper import ExitoRegistro
from ..serializers.usuarios_serializers import  UsuarioSerializer, LoginSerializer
from api.models import Usuario
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password , check_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiSchemaBase
from drf_spectacular.types import OpenApiTypes

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

@extend_schema(methods=['POST'], request=UsuarioSerializer, responses={201: UsuarioSerializer}, tags=['Usuario'], description='Registrar un usuario')
@api_view(['POST'])
def registrarUsuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data['password']
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        usuario = serializer.save()
        
        refresh = RefreshToken.for_user(usuario)

        return Response({'status_code': ExitoRegistro.CODIGO.value,'message': ExitoRegistro.REGISTRO_EXITOSO.value}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(methods=['POST'], request=LoginSerializer, responses={200: UsuarioSerializer}, tags=['Usuario'], description='Iniciar sesión como usuario')
@api_view(['POST'])
def loginUsuario(request):
    try:
        usuario = get_object_or_404(Usuario, usuario=request.data['usuario'])
        password = request.data['password']

        if check_password(password, usuario.password):
            refresh = RefreshToken.for_user(usuario)

            return Response({'status_code': ExitoLogin.CODIGO.value,'token': str(refresh.access_token), 'usuario': UsuarioSerializer(usuario).data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': ErroresLogin.MENSAJE.value}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'message': ErroresLogin.CREDECIALES_INCOMPLETAS.value}, status=status.HTTP_400_BAD_REQUEST)
    except Usuario.DoesNotExist:
        return Response({'message': ErroresLogin.USUARIO_NO_ENCONTRADO.value}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(methods=['POST'], request=UsuarioSerializer, responses={201: UsuarioSerializer}, tags=['Administrador'], description='Registrar un administrador')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrarAdmin(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['tipoUsuario'] = TipoUsuario.ADMIN.value
        password = serializer.validated_data['password']
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        admin_fields = ['usuario', 'nombre', 'apellidoMaterno', 'apellidoPaterno', 'correo', 'fechaRegistro', 'tipoUsuario']
        usuario_data = {key: serializer.validated_data.get(key, None) for key in admin_fields}
        usuario = Usuario.objects.create(**usuario_data)
        refresh = RefreshToken.for_user(usuario)

        return Response({'status_code': ExitoRegistro.CODIGO.value, 'message': ExitoRegistro.REGISTRO_EXITOSO.value}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(methods=['POST'], request=LoginSerializer, responses={200: UsuarioSerializer}, tags=['Administrador'], description='Iniciar sesión como administrador')
@api_view(['POST'])
def loginAdministrador(request):
    try:
        usuario = get_object_or_404(Usuario, usuario=request.data['usuario'])
        password = request.data['password']
        
        if usuario.tipoUsuario != TipoUsuario.ADMIN.value:
            return Response({'message': ErroresLogin.USUARIO_NO_ADMIN.value}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, usuario.password):
            refresh = RefreshToken.for_user(usuario)

            return Response({'status_code': ExitoLogin.CODIGO.value,'token': str(refresh.access_token), 'usuario': UsuarioSerializer(usuario).data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': ErroresLogin.MENSAJE.value}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'message': ErroresLogin.CREDECIALES_INCOMPLETAS.value}, status=status.HTTP_400_BAD_REQUEST)
    except Usuario.DoesNotExist:
        return Response({'message': ErroresLogin.USUARIO_NO_ENCONTRADO.value}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
