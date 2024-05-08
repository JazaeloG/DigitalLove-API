import json
from channels.generic.websocket import AsyncWebsocketConsumer

from api.models import Usuario
from chatApp.models import MensajeChatPersonal

class chatConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'name':name
            }
        )
    async def chat_message(self,event):
        message = event['message']
        name = event['name']

        await self.send(text_data=json.dumps({
            'message':message,
            'name':name
        }))

from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user = await self.get_user(self.user_id)
        if self.user.is_anonymous:
            await self.close()
        else:
            self.room_group_name = f'notifications_{self.user_id}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'notification': notification
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return Usuario.objects.get(id=user_id)



class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_personal_id = self.scope['url_route']['kwargs']['chat_personal_id']
        self.chat_personal_group_name = f'personal_chat_{self.chat_personal_id}'

        await self.channel_layer.group_add(
            self.chat_personal_group_name,
            self.channel_name
        )

        await self.send_previous_messages()

        await self.accept()
    
    async def send_previous_messages(self):
        
        previous_messages = MensajeChatPersonal.objects.filter(chat_personal_id=self.chat_personal_id)

        for message in previous_messages:
            await self.send(text_data=json.dumps({
                'message': message.mensaje,
                'sender_id': message.sender_id.id,
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_personal_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']

        message_instance = MensajeChatPersonal.objects.create(
            chat_personal_id=self.chat_personal_id,
            sender_id=sender_id, 
            recipient_id=self.scope['user'].id,  
            mensaje=message
        )

        # Enviar el mensaje al grupo
        await self.channel_layer.group_send(
            self.chat_personal_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
        }))