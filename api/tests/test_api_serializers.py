import pytest
from api.models import Usuario, MotivosReporte, TipoUsuario, EstadoUsuario, SexoUsuario, EstadosMexico
from api.serializers.usuarios_serializers import UsuarioSerializer, LoginSerializer
from api.serializers.match_serializers import LikeSerializer, MatchSerializer
from api.serializers.reporte_serializer import ReporteSerializer


@pytest.mark.django_db
def test_usuario_serializer():
    data = {
        "tipoUsuario": TipoUsuario.USUARIO.value,
        "nombre": "Juan",
        "apellidoMaterno": "Pérez",
        "apellidoPaterno": "González",
        "edad": 25,
        "ubicacion": EstadosMexico.CIUDAD_DE_MEXICO.name,
        "sexo": SexoUsuario.MASCULINO.value,
        "telefono": "1234567890",
        "usuario": "juan123",
        "estado": EstadoUsuario.ACTIVO.value,
        "correo": "juan@example.com",
        "password": "password123",
        "fechaRegistro": "2024-05-17T12:00:00Z"
    }
    serializer = UsuarioSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.nombre == "Juan"
    assert user.apellidoMaterno == "Pérez"
    assert user.apellidoPaterno == "González"
    assert user.edad == 25
    assert user.ubicacion == EstadosMexico.CIUDAD_DE_MEXICO.name
    assert user.sexo == SexoUsuario.MASCULINO.value
    assert user.telefono == "1234567890"
    assert user.usuario == "juan123"
    assert user.estado == EstadoUsuario.ACTIVO.value
    assert user.correo == "juan@example.com"

@pytest.mark.django_db
def test_login_serializer():
    data = {
        "usuario": "juan123",
        "password": "password123"
    }
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_like_serializer():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.name,
        sexo=SexoUsuario.MASCULINO.value,
        telefono="1234567890",
        usuario="juan123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="juan@example.com",
        password="password123"
    )
    user2 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Ana",
        apellidoMaterno="Martínez",
        apellidoPaterno="López",
        edad=30,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.name,
        sexo=SexoUsuario.FEMENINO.value,
        telefono="0987654321",
        usuario="ana123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="ana@example.com",
        password="password123"
    )
    data = {"envia": user1.id, "recibe": user2.id}
    serializer = LikeSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    like = serializer.save()
    assert like.envia == user1
    assert like.recibe == user2

@pytest.mark.django_db
def test_match_serializer():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.name,
        sexo=SexoUsuario.MASCULINO.value,
        telefono="1234567890",
        usuario="juan123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="juan@example.com",
        password="password123"
    )
    user2 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Ana",
        apellidoMaterno="Martínez",
        apellidoPaterno="López",
        edad=30,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.name,
        sexo=SexoUsuario.FEMENINO.value,
        telefono="0987654321",
        usuario="ana123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="ana@example.com",
        password="password123"
    )
    data = {"envia_id": user1.id, "recibe_id": user2.id, "accion": True}
    serializer = MatchSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_reporte_serializer():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.name,
        sexo=SexoUsuario.MASCULINO.value,
        telefono="1234567890",
        usuario="juan123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="juan@example.com",
        password="password123"
    )
    data = {
        "usuario_reportado": user1.id,
        "motivo": MotivosReporte.SPAM.name,
        "comentario": "Comentario de prueba",
        "fechaRegistro": "2024-05-17T12:00:00Z"
    }
    serializer = ReporteSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    reporte = serializer.save()
    assert reporte.usuario_reportado == user1
    assert reporte.motivo == MotivosReporte.SPAM.name
    assert reporte.comentario == "Comentario de prueba"
