from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from api.enums.tipo_usuario import TipoUsuario
from api.enums.estado_usuario import EstadoUsuario
from api.helpers.login_helper import ErroresLogin, ExitoLogin
from api.helpers.registro_helper import ErroresRegistro, ExitoRegistro
from api.helpers.reporte_helper import BloqueoHelper
from api.helpers.usuario_helper import ExitoUsuario, ErroresUsuario
from api.views.methods.register_methods import validar_formato_telefono
from ..serializers.usuarios_serializers import AgregarFotoSerializer, EliminarFotoSerializer, PreferenciasUsuarioSerializer, UsuarioBloquearSerializer, UsuarioSerializer, LoginSerializer, UsuarioAdminSerializer
from api.models import FotoUsuario, PreferenciasUsuario, Usuario
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.contrib.auth.hashers import make_password , check_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

@extend_schema(methods=['POST'], request=UsuarioSerializer, responses={201: UsuarioSerializer}, tags=['Usuario'], description='Registrar un usuario')
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, FileUploadParser])
def registrarUsuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        telefono = request.data.get('telefono')
        if not validar_formato_telefono(telefono):
            return Response({'message': ErroresRegistro.FORMATO_TELEFONO.value}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data['password']
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        usuario = serializer.save()

        fotos_data = request.FILES.getlist('fotos')
        for foto_data in fotos_data:
            FotoUsuario.objects.create(usuario=usuario, foto=foto_data)

        refresh = RefreshToken.for_user(usuario)
        return Response({
            'status_code': ExitoRegistro.CODIGO.value,
            'message': ExitoRegistro.REGISTRO_EXITOSO.value,
            'usuario': UsuarioSerializer(usuario).data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(methods=['POST'], request=LoginSerializer, responses={200: UsuarioSerializer}, tags=['Usuario'], description='Iniciar sesión como usuario')
@api_view(['POST'])
def loginUsuario(request):
    try:
        usuario = get_object_or_404(Usuario, usuario=request.data['usuario'])
        password = request.data['password']

        if usuario.estado == EstadoUsuario.BLOQUEADO.value:
            return Response({'message': ErroresLogin.CUENTA_BLOQUEADA.value}, status=status.HTTP_403_FORBIDDEN)
        elif usuario.estado == EstadoUsuario.ELIMINADO.value:
            return Response({'message': ErroresLogin.CUENTA_ELIMINADA.value}, status=status.HTTP_403_FORBIDDEN)

        if check_password(password, usuario.password):
            refresh = RefreshToken.for_user(usuario)
            return Response({'status_code': ExitoLogin.CODIGO.value, 'token': str(refresh.access_token), 'usuario': UsuarioSerializer(usuario).data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': ErroresLogin.MENSAJE.value}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'message': ErroresLogin.CREDECIALES_INCOMPLETAS.value}, status=status.HTTP_400_BAD_REQUEST)
    except Usuario.DoesNotExist:
        return Response({'message': ErroresLogin.USUARIO_NO_ENCONTRADO.value}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(methods=['POST'], request=UsuarioAdminSerializer, responses={201: UsuarioSerializer}, tags=['Administrador'], description='Registrar un administrador')
@api_view(['POST'])
def registrarAdmin(request):
    serializer = UsuarioAdminSerializer(data=request.data)
    if serializer.is_valid():
        usuario_data = serializer.validated_data
        usuario_data['tipoUsuario'] = TipoUsuario.ADMIN.value
        usuario_data['password'] = make_password(usuario_data['password'])
        usuario = Usuario.objects.create(**usuario_data)
        refresh = RefreshToken.for_user(usuario)
        serializer = UsuarioSerializer(usuario)
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

@extend_schema(methods=['GET'], tags=['Usuario'], description='Obtener usuarios tipo USUARIO', responses={200: UsuarioSerializer})
@api_view(['GET'])
def get_usuarios_usuario(request):
    usuarios = Usuario.objects.filter(tipoUsuario=TipoUsuario.USUARIO.value)
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)

@extend_schema(methods=['GET'], tags=['Administrador'], description='Obtener usuarios tipo ADMIN', responses={200: UsuarioSerializer})
@api_view(['GET'])
def get_usuarios_admin(request):
    usuarios = Usuario.objects.filter(tipoUsuario=TipoUsuario.ADMIN.value)
    serializer = UsuarioAdminSerializer(usuarios, many=True)
    return Response(serializer.data)


@extend_schema(methods=['POST'], tags=['Usuario'], description='Bloquear un usuario', responses={200: UsuarioSerializer})
@api_view(['POST'])
def bloquear_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
    except Usuario.DoesNotExist:
        return Response({'message': ErroresLogin.USUARIO_NO_ENCONTRADO.value}, status=status.HTTP_404_NOT_FOUND)
    if usuario.estado == EstadoUsuario.BLOQUEADO.value:
        return Response({'message': BloqueoHelper.BLOQUE_REPETIDO.value}, status=status.HTTP_400_BAD_REQUEST)

    usuario.estado = EstadoUsuario.BLOQUEADO.value
    usuario.save()

    return Response({'message': BloqueoHelper.BLOQUEO_REGISTRADO.value}, status=status.HTTP_200_OK)


@extend_schema(methods=['PATCH'], tags=['Usuario'], description='Actualizar un usuario', request=UsuarioSerializer, responses={200: UsuarioSerializer})
@api_view(['PATCH'])
def actualizar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response({"message": ErroresUsuario.USUARIO_NO_ENCONTRADO.value}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": ExitoUsuario.USUARIO_ACTUALIZADO.value})
    return Response({"message": ErroresUsuario.USUARIO_NO_ACTUALIZADO.value}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['POST'],
    tags=['Preferencias'],
    description='Registrar o actualizar preferencias de usuario',
    request=PreferenciasUsuarioSerializer,
    responses={200: PreferenciasUsuarioSerializer}
)
@api_view(['POST'])
def registrar_preferencias(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        serializer = PreferenciasUsuarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        preferencias, created = PreferenciasUsuario.objects.update_or_create(
            usuario=usuario,
            defaults=serializer.validated_data
        )

        return Response({"message": ExitoUsuario.PREFERENCIAS_REGISTRADAS.value}, status=status.HTTP_200_OK)
    
    except Usuario.DoesNotExist:
        return Response({'error': ErroresUsuario.PREFERENCIAS_NO_ENCONTRADAS.value}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    methods=['PATCH'],
    tags=['Preferencias'],
    description='Actualizar preferencias de usuario',
    request=PreferenciasUsuarioSerializer,
    responses={200: PreferenciasUsuarioSerializer}
)
@api_view(['PATCH'])
def actualizar_preferencias(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        preferencias = PreferenciasUsuario.objects.get(usuario=usuario)
        serializer = PreferenciasUsuarioSerializer(preferencias, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": ExitoUsuario.PREFERENCIAS_ACTUALIZADAS.value}, status=status.HTTP_200_OK)
    
    except Usuario.DoesNotExist:
        return Response({'error': ErroresUsuario.USUARIO_NO_ENCONTRADO.value}, status=status.HTTP_404_NOT_FOUND)
    except PreferenciasUsuario.DoesNotExist:
        return Response({'error': ErroresUsuario.PREFERENCIAS_NO_ENCONTRADAS.value}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@extend_schema(
    methods=['DELETE'],
    tags=['Usuario'],
    description='Eliminar foto de usuario',
    request=EliminarFotoSerializer,
    responses={200: UsuarioSerializer}
)

@api_view(['DELETE'])
def eliminarFotoUsuario(request, usuario_id, foto_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        foto = FotoUsuario.objects.get(id=foto_id, usuario=usuario)
        foto.delete()
        return Response({'message': ExitoUsuario.FOTO_ELIMINADA.value}, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response({'error': ErroresUsuario.USUARIO_NO_ENCONTRADO.value, "usuario": usuario}, status=status.HTTP_404_NOT_FOUND)
    except FotoUsuario.DoesNotExist:
        return Response({'error': ErroresUsuario.FOTO_NO_ENCONTRADA.value}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    methods=['POST'],
    tags=['Usuario'],
    description='Agregar foto a usuario',
    request=AgregarFotoSerializer,
    responses={201: UsuarioSerializer}
)
@api_view(['POST'])
def agregarFotoUsuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        foto_data = request.FILES.get('foto')
        FotoUsuario.objects.create(usuario=usuario, foto=foto_data)
        return Response({'message': ExitoUsuario.FOTO_REGISTRADA.value}, status=status.HTTP_201_CREATED)
    except Usuario.DoesNotExist:
        return Response({'message': ErroresUsuario.USUARIO_NO_ENCONTRADO.value}, status=status.HTTP_404_NOT_FOUND)