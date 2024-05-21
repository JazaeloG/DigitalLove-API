import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import Usuario
from asgiref.sync import sync_to_async
from chatApp.models import ChatPersonal, MensajeChat, Notificacion
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        chat_personal_id = self.scope['url_route']['kwargs']['chat_personal_id']
        self.chat_personal_group_name = f'chat_personal_{chat_personal_id}'

        await self.channel_layer.group_add(
            self.chat_personal_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None):
        received_data_json = json.loads(text_data)
        mensaje = received_data_json.get('mensaje')
        usuario_envia_id = received_data_json.get('usuario_envia_id')
        usuario_recibe_id = received_data_json.get('usuario_recibe_id')
        chat_personal_id = received_data_json.get('chat_personal_id')
        if not mensaje:
            return False
        
        usuario_envia = await self.get_usuario_object(usuario_envia_id)
        usuario_recibe = await self.get_usuario_object(usuario_recibe_id)
        chat_personal = await self.get_chat_personal(chat_personal_id)

        if not usuario_envia or not usuario_recibe or not chat_personal:
            return False

        await self.crear_mensaje_chat(chat_personal, usuario_envia, mensaje)

        otro_usuario_chat_room = f'user_chatroom_{usuario_recibe.id}'
        response = {
            'mensaje': mensaje,
            'usuario_envia': usuario_envia.id,
            'chat_personal_id': chat_personal_id
        }

        await self.channel_layer.group_send(
            otro_usuario_chat_room,
            {
                'type': 'mensaje_chat',
                'mensaje': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_personal_group_name,
            {
                'type': 'mensaje_chat',
                'mensaje': json.dumps(response)
            }
        )

        # Ejemplo de creación de reporte y envío de notificación al grupo de administradores
        if self.should_report_message(mensaje):  # Implementa tu lógica de reporte aquí
            report_data = {
                'mensaje': mensaje,
                'usuario_envia': usuario_envia.id,
                'chat_personal_id': chat_personal_id,
                'timestamp': datetime.now().isoformat()
            }
            await self.channel_layer.group_send(
                'admin_reports',
                {
                    'type': 'send_report_notification',
                    'report': report_data
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_personal_group_name,
            self.channel_name
        )

    async def mensaje_chat(self, event):
        await self.send(text_data=event['mensaje'])

    async def should_report_message(self, mensaje):
        # Implementa tu lógica para determinar si un mensaje debe ser reportado
        return 'inapropiado' in mensaje.lower()  # Ejemplo simple

    @database_sync_to_async
    def get_usuario_object(self, usuario_id):
        return Usuario.objects.filter(id=usuario_id).first()
    
    @database_sync_to_async
    def get_chat_personal(self, chat_personal_id):
        return ChatPersonal.objects.filter(id=chat_personal_id).first()
    
    @database_sync_to_async
    def crear_mensaje_chat(self, chat, usuario, mensaje):
        MensajeChat.objects.create(chat=chat, usuario=usuario, mensaje=mensaje)


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

    async def send_report_notification(self, report_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_report_notification',
                'report': report_data
            }
        )

    async def send_notification(self, notification_data):
        notificacion = await self.create_notification(notification_data)
        
        await self.channel_layer.send(
            f'user_notifications_{notification_data["usuario_recibe_id"]}',
            {
                'type': 'send_notification',
                'notification': {
                    'mensaje': notification_data['mensaje'],
                    'fecha_creacion': notificacion.fecha_creacion.isoformat()
                }
            }
        )

    @database_sync_to_async
    def create_notification(self, notification_data):
        return Notificacion.objects.create(
            usuario_envia_id=notification_data['usuario_envia_id'],
            usuario_recibe_id=notification_data['usuario_recibe_id'],
            mensaje=notification_data['mensaje']
        )

    @database_sync_to_async
    def get_user(self, user_id):
        return Usuario.objects.get(id=user_id)
    

class AdminReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'admin_reports'
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

    async def send_report_notification(self, event):
        report_data = event['report']
        await self.send(text_data=json.dumps(report_data))
