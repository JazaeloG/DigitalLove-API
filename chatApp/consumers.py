import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import Usuario
from asgiref.sync import sync_to_async
from chatApp.models import ChatPersonal, MensajeChat, Notificacion
from api.models import Reporte 
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
            return

        usuario_envia = await self.get_usuario_object(usuario_envia_id)
        usuario_recibe = await self.get_usuario_object(usuario_recibe_id)
        chat_personal = await self.get_chat_personal(chat_personal_id)

        if not usuario_envia or not usuario_recibe or not chat_personal:
            return
        
        await self.crear_mensaje_chat(chat_personal, usuario_envia, mensaje)

        response = {
            'mensaje': mensaje,
            'usuario_envia': usuario_envia.id,
            'chat_personal_id': chat_personal_id
        }

        await self.channel_layer.group_send(
            self.chat_personal_group_name,
            {
                'type': 'mensaje_chat',
                'mensaje': json.dumps(response)
            }
        )
        report_data = {
            'mensaje': f'Usuario {usuario_envia.id} reportado en el chat {chat_personal_id}',
            'usuario_envia_id': usuario_envia.id,
            'usuario_recibe_id': usuario_recibe.id,
            'chat_personal_id': chat_personal_id
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

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps(data))

    async def notification_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None

    @database_sync_to_async
    def create_notification(self, data):
        return Notificacion.objects.create(
            usuario_envia_id=data['usuario_envia_id'],
            usuario_recibe_id=data['usuario_recibe_id'],
            mensaje=data['mensaje']
        )
class AdminReportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'admin_reports'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None):
        received_data_json = json.loads(text_data)
        usuario_reportado_id = received_data_json.get('usuario_reportado_id')
        motivo = received_data_json.get('motivo')
        comentario = received_data_json.get('comentario')

        usuario_reportado = await self.get_usuario_object(usuario_reportado_id)
        if not usuario_reportado:
            return

        report = await self.create_admin_report(usuario_reportado, motivo, comentario)

        report_data = {
            'usuario_reportado_id': usuario_reportado.id,
            'motivo': motivo,
            'comentario': comentario,
            'fechaRegistro': report.fechaRegistro.isoformat()
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_report_notification',
                'report': report_data
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_usuario_object(self, usuario_id):
        return Usuario.objects.filter(id=usuario_id).first()

    @database_sync_to_async
    def create_admin_report(self, usuario_reportado, motivo, comentario):
        return Reporte.objects.create(
            usuario_reportado=usuario_reportado,
            motivo=motivo,
            comentario=comentario
        )

    async def send_report_notification(self, event):
        report_data = event['report']
        await self.send(text_data=json.dumps(report_data))
