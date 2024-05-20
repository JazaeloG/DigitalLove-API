import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from chatApp.models import ChatPersonal
from chatApp.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter

User = get_user_model()

@pytest.fixture
async def setup_users_and_chat():
    user1 = await sync_to_async(User.objects.create_user)(
        usuario='test_user1', password='password1', email='test_user1@example.com', tipoUsuario='USUARIO'
    )
    user2 = await sync_to_async(User.objects.create_user)(
        usuario='test_user2', password='password2', email='test_user2@example.com', tipoUsuario='USUARIO'
    )
    chat = await sync_to_async(ChatPersonal.objects.create)(
        usuario=user1, usuario_match=user2
    )
    return user1, user2, chat

@pytest.mark.django_db
@pytest.mark.asyncio
class TestChatConsumer:
    async def test_connect(self):
        communicator = WebsocketCommunicator(
            ProtocolTypeRouter({
                'websocket': URLRouter(websocket_urlpatterns),
            }),
            "/ws/chat/1/"
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_receive_message(self, setup_users_and_chat):
        user1, user2, chat = setup_users_and_chat

        communicator = WebsocketCommunicator(
            ProtocolTypeRouter({
                'websocket': URLRouter(websocket_urlpatterns),
            }),
            f"/ws/chat/{chat.id}/"
        )
        connected, _ = await communicator.connect()
        assert connected

        message = {
            'mensaje': 'Hola',
            'usuario_envia_id': user1.id,
            'usuario_recibe_id': user2.id,
            'chat_personal_id': chat.id
        }

        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()

        assert response['mensaje'] == 'Hola'
        assert response['usuario_envia'] == user1.id
        assert response['chat_personal_id'] == chat.id

        await communicator.disconnect()

@pytest.mark.django_db
@pytest.mark.asyncio
class TestNotificationConsumer:
    async def test_connect(self):
        communicator = WebsocketCommunicator(
            ProtocolTypeRouter({
                'websocket': URLRouter(websocket_urlpatterns),
            }),
            "/ws/notifications/1/"
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_send_notification(self, setup_users_and_chat):
        user1, user2, _ = setup_users_and_chat

        communicator = WebsocketCommunicator(
            ProtocolTypeRouter({
                'websocket': URLRouter(websocket_urlpatterns),
            }),
            f"/ws/notifications/{user2.id}/"
        )
        connected, _ = await communicator.connect()
        assert connected

        channel_layer = get_channel_layer()
        notification_data = {
            'usuario_envia_id': user1.id,
            'usuario_recibe_id': user2.id,
            'mensaje': 'Nueva notificación'
        }

        await channel_layer.group_send(
            f'notifications_{user2.id}',
            {
                'type': 'send_notification',
                'notification': notification_data
            }
        )

        response = await communicator.receive_json_from()

        assert response['mensaje'] == 'Nueva notificación'

        await communicator.disconnect()
