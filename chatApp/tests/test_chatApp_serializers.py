import pytest
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.timezone import now as timezone_now, utc
from chatApp.models import ChatPersonal, MensajeChat, Notificacion
from chatApp.serializers.chat_serializers import ChatPersonalSerializer, MensajeChatSerializer
from chatApp.serializers.notification_serializers import NotificacionSerializer

User = get_user_model()

@pytest.fixture
def create_user():
    user = User.objects.create_user(
        usuario='testuser',
        email='test@example.com',
        password='testpassword'
    )
    return user

@pytest.fixture
def create_chat_personal(create_user):
    user1 = create_user
    user2 = User.objects.create_user(
        usuario='testuser2',
        email='test2@example.com',
        password='testpassword'
    )
    chat = ChatPersonal.objects.create(
        usuario=user1,
        usuario_match=user2,
        fechaRegistro=timezone_now().replace(microsecond=0)
    )
    return chat

@pytest.fixture
def create_mensaje_chat(create_chat_personal):
    chat = create_chat_personal
    user = User.objects.get(usuario='testuser')
    mensaje = MensajeChat.objects.create(
        chat=chat,
        usuario=user,
        mensaje='Test message',
        fechaRegistro=timezone_now().replace(microsecond=0)
    )
    return mensaje

@pytest.fixture
def create_notificacion(create_user):
    user_envia = create_user
    user_recibe = User.objects.create_user(
        usuario='testuser3',
        email='test3@example.com',
        password='testpassword'
    )
    notificacion = Notificacion.objects.create(
        usuario_envia_id=user_envia,
        usuario_recibe_id=user_recibe,
        mensaje='Test notification',
        fecha_creacion=timezone_now().replace(microsecond=0)
    )
    return notificacion

def normalize_datetime(datetime_obj):
    return datetime_obj.astimezone(utc).isoformat().replace("+00:00", "Z")

@pytest.mark.django_db
def test_chat_personal_serializer(create_chat_personal):
    chat = create_chat_personal
    serializer = ChatPersonalSerializer(chat)
    assert serializer.data['fechaRegistro'] == normalize_datetime(chat.fechaRegistro)

@pytest.mark.django_db
def test_mensaje_chat_serializer(create_mensaje_chat):
    mensaje = create_mensaje_chat
    serializer = MensajeChatSerializer(mensaje)
    assert serializer.data['fechaRegistro'] == normalize_datetime(mensaje.fechaRegistro)

@pytest.mark.django_db
def test_notificacion_serializer(create_notificacion):
    notificacion = create_notificacion
    serializer = NotificacionSerializer(notificacion)
    assert serializer.data['fecha_creacion'] == normalize_datetime(notificacion.fecha_creacion)
