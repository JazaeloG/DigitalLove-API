import pytest
from django.db import IntegrityError
from api.models import Usuario
from chatApp.models import ChatPersonal, MensajeChat, Notificacion

@pytest.mark.django_db
def test_chat_personal_creation():
    user1 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User1",
        apellidoPaterno="Apellido1",
        edad=25,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='MASCULINO',
        telefono="1234567890",
        usuario="user1",
        estado='ACTIVO',
        correo="user1@example.com",
        password="password123"
    )
    
    user2 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User2",
        apellidoPaterno="Apellido2",
        edad=26,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='FEMENINO',
        telefono="0987654321",
        usuario="user2",
        estado='ACTIVO',
        correo="user2@example.com",
        password="password123"
    )
    
    chat = ChatPersonal.objects.create(usuario=user1, usuario_match=user2)
    
    assert chat.usuario == user1
    assert chat.usuario_match == user2
    assert chat.actualizado is not None
    assert chat.fechaRegistro is not None

@pytest.mark.django_db
def test_chat_personal_unique_constraint():
    user1 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User1",
        apellidoPaterno="Apellido1",
        edad=25,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='MASCULINO',
        telefono="1234567890",
        usuario="user1",
        estado='ACTIVO',
        correo="user1@example.com",
        password="password123"
    )
    
    user2 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User2",
        apellidoPaterno="Apellido2",
        edad=26,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='FEMENINO',
        telefono="0987654321",
        usuario="user2",
        estado='ACTIVO',
        correo="user2@example.com",
        password="password123"
    )
    
    ChatPersonal.objects.create(usuario=user1, usuario_match=user2)
    
    with pytest.raises(IntegrityError):
        ChatPersonal.objects.create(usuario=user1, usuario_match=user2)

@pytest.mark.django_db
def test_mensaje_chat_creation():
    user1 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User1",
        apellidoPaterno="Apellido1",
        edad=25,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='MASCULINO',
        telefono="1234567890",
        usuario="user1",
        estado='ACTIVO',
        correo="user1@example.com",
        password="password123"
    )
    
    user2 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User2",
        apellidoPaterno="Apellido2",
        edad=26,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='FEMENINO',
        telefono="0987654321",
        usuario="user2",
        estado='ACTIVO',
        correo="user2@example.com",
        password="password123"
    )
    
    chat = ChatPersonal.objects.create(usuario=user1, usuario_match=user2)
    
    mensaje = MensajeChat.objects.create(chat=chat, usuario=user1, mensaje="Hola, User2")
    
    assert mensaje.chat == chat
    assert mensaje.usuario == user1
    assert mensaje.mensaje == "Hola, User2"
    assert mensaje.fechaRegistro is not None

@pytest.mark.django_db
def test_notificacion_creation():
    user1 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User1",
        apellidoPaterno="Apellido1",
        edad=25,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='MASCULINO',
        telefono="1234567890",
        usuario="user1",
        estado='ACTIVO',
        correo="user1@example.com",
        password="password123"
    )
    
    user2 = Usuario.objects.create(
        tipoUsuario='USUARIO',
        nombre="User2",
        apellidoPaterno="Apellido2",
        edad=26,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='FEMENINO',
        telefono="0987654321",
        usuario="user2",
        estado='ACTIVO',
        correo="user2@example.com",
        password="password123"
    )
    
    notificacion = Notificacion.objects.create(usuario_envia_id=user1, usuario_recibe_id=user2, mensaje="Notificación 1")
    
    assert notificacion.usuario_envia_id == user1
    assert notificacion.usuario_recibe_id == user2
    assert notificacion.mensaje == "Notificación 1"
    assert notificacion.fecha_creacion is not None

@pytest.mark.django_db
def test_chat_by_user_method():
    user1 = Usuario.objects.create(
        usuario="user1",
        tipoUsuario='USUARIO',
        nombre="User1",
        apellidoPaterno="Apellido1",
        edad=25,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='MASCULINO',
        telefono="1234567890",
        estado='ACTIVO',
        correo="user1@example.com",
        password="password123"
    )
    user2 = Usuario.objects.create(
        usuario="user2",
        tipoUsuario='USUARIO',
        nombre="User2",
        apellidoPaterno="Apellido2",
        edad=26,
        ubicacion="CIUDAD_DE_MEXICO",
        sexo='FEMENINO',
        telefono="0987654321",
        estado='ACTIVO',
        correo="user2@example.com",
        password="password123"
    )
    chat1 = ChatPersonal.objects.create(usuario=user1, usuario_match=user2)
    chat2 = ChatPersonal.objects.create(usuario=user2, usuario_match=user1)
    
    user1_chats = ChatPersonal.objects.by_user(user1)
    assert chat1 in user1_chats
    assert chat2 in user1_chats
    
    user2_chats = ChatPersonal.objects.by_user(user2)
    assert chat1 in user2_chats
    assert chat2 in user2_chats

