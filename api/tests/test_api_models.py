import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from api.enums.estados_pais import EstadosMexico
from api.enums.motivos_reporte_ import MotivosReporte
from api.models import Usuario, EstadoUsuario, SexoUsuario, TipoUsuario, Like, Match, Reporte


@pytest.mark.django_db
def test_usuario_str():
    user = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
        sexo=SexoUsuario.MASCULINO.value,
        telefono="1234567890",
        usuario="juan123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="juan@example.com",
        password="password123"
    )
    assert str(user) == "Juan"

@pytest.mark.django_db
def test_usuario_validation_error():
    with pytest.raises(ValidationError):
        user = Usuario(
            tipoUsuario=TipoUsuario.USUARIO.value,
            nombre="", # nombre vacio, mostrar error
            apellidoMaterno="Pérez",
            apellidoPaterno="González",
            edad=17,  # edad invalida, debe ser mayor a 18, mostrar error
            ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
            sexo=SexoUsuario.MASCULINO.value,
            telefono="123",
            usuario="juan123",
            estado=EstadoUsuario.ACTIVO.value,
            correo="juan@example.com",
            password="password123"
        )
        user.full_clean()

@pytest.mark.django_db

def test_create_superuser():
    
    user = Usuario.objects.create_superuser(
        usuario="admin",
        email="admin@example.com",
        password="admin123",
    )

@pytest.mark.django_db
def test_like_creation():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
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
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
        sexo=SexoUsuario.FEMENINO.value,
        telefono="0987654321",
        usuario="ana123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="ana@example.com",
        password="password123"
    )
    like = Like.objects.create(envia=user1, recibe=user2)
    assert like.envia == user1
    assert like.recibe == user2
    assert not like.aceptado

@pytest.mark.django_db
def test_match_creation():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
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
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
        sexo=SexoUsuario.FEMENINO.value,
        telefono="0987654321",
        usuario="ana123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="ana@example.com",
        password="password123"
    )
    match = Match.objects.create(usuario1=user1, usuario2=user2)
    assert match.usuario1 == user1
    assert match.usuario2 == user2

@pytest.mark.django_db
def test_match_clean():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
        sexo=SexoUsuario.MASCULINO.value,
        telefono="1234567890",
        usuario="juan123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="juan@example.com",
        password="password123"
    )
    with pytest.raises(ValidationError):
        match = Match(usuario1=user1, usuario2=user1)
        match.clean()

@pytest.mark.django_db
def test_reporte_creation():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
        sexo=SexoUsuario.MASCULINO.value,
        telefono="1234567890",
        usuario="juan123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="juan@example.com",
        password="password123"
    )
    reporte = Reporte.objects.create(
        usuario_reportado=user1,
        motivo=MotivosReporte.SPAM.value,
        comentario="Comentario de prueba"
    )
    assert reporte.usuario_reportado == user1
    assert reporte.motivo == MotivosReporte.SPAM.value
    assert reporte.comentario == "Comentario de prueba"

@pytest.mark.django_db
def test_reporte_clean():
    user1 = Usuario.objects.create(
        tipoUsuario=TipoUsuario.USUARIO.value,
        nombre="Juan",
        apellidoMaterno="Pérez",
        apellidoPaterno="González",
        edad=25,
        ubicacion=EstadosMexico.CIUDAD_DE_MEXICO.value,
        sexo=SexoUsuario.MASCULINO.value,
        telefono="1234567890",
        usuario="juan123",
        estado=EstadoUsuario.ACTIVO.value,
        correo="juan@example.com",
        password="password123"
    )
    with pytest.raises(ValidationError):
        reporte = Reporte(usuario_reportado=user1, motivo="", comentario="Comentario")
        reporte.clean()

