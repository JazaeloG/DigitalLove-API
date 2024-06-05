import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from chatApp.models import ChatPersonal, MensajeChat, Notificacion
from chatApp.serializers.chat_serializers import ChatPersonalSerializer, MensajeChatSerializer
from chatApp.serializers.notification_serializers import NotificacionSerializer

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_get_user_chats(api_client):
    user_id = 1
    mixer.blend(ChatPersonal, usuario_id=user_id)
    mixer.blend(ChatPersonal, usuario_match_id=user_id)

    url = reverse('get_user_chats', kwargs={'usuario_id': user_id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    
    chats = ChatPersonal.objects.filter(usuario_id=user_id) | ChatPersonal.objects.filter(usuario_match_id=user_id)
    serializer = ChatPersonalSerializer(chats, many=True)
    assert response.data == {"chats": serializer.data}

@pytest.mark.django_db
def test_obtener_mensajes_anteriores(api_client):
    chat_personal = mixer.blend(ChatPersonal)
    mixer.blend(MensajeChat, chat=chat_personal)

    url = reverse('obtener_mensajes_anteriores', kwargs={'chat_personal_id': chat_personal.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    
    mensajes = MensajeChat.objects.filter(chat=chat_personal.id).order_by('fechaRegistro')
    serializer = MensajeChatSerializer(mensajes, many=True)
    assert response.data == {'mensajes': serializer.data}

@pytest.mark.django_db
def test_listar_notificaciones(api_client):
    user_id = 1
    mixer.blend(Notificacion, usuario_id=user_id)

    url = reverse('listar_notificaciones', kwargs={'usuario_id': user_id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    
    notificaciones = Notificacion.objects.filter(usuario_id=user_id)
    serializer = NotificacionSerializer(notificaciones, many=True)
    assert response.data == serializer.data

@pytest.mark.django_db
def test_enviar_notificacion(api_client):
    user = mixer.blend('api.Usuario')
    data = {'notification': 'Test notification'}

    url = reverse('enviar_notificacion', kwargs={'user_id': user.id})
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_send_report_to_admin(api_client):
    mixer.blend('api.Usuario', tipoUsuario='ADMIN')
    data = {'reporte': 'Test report'}

    url = reverse('send_report_to_admin')
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
