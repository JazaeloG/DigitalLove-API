import asyncio
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from api.enums.estado_usuario import EstadoUsuario
from api.enums.tipo_usuario import TipoUsuario
from api.models import Usuario, Like, Match, Reporte
from chatApp.models import ChatPersonal 
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from unittest.mock import patch
from datetime import datetime

class LikeUserTest(APITestCase):
    def setUp(self):
        self.envia_user = Usuario.objects.create(usuario="envia_user")
        self.recibe_user = Usuario.objects.create(usuario="recibe_user")
        self.url = reverse('like_user')
    
    def test_like_user_success(self):
        data = {"envia": self.envia_user.id, "recibe": self.recibe_user.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Like enviado correctamente")
        self.assertTrue(Like.objects.filter(envia_id=self.envia_user.id, recibe_id=self.recibe_user.id).exists())

    def test_like_user_user_not_found(self):
        data = {"envia": 999, "recibe": self.recibe_user.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "El usuario recepto no existe")

    def test_like_user_already_liked(self):
        Like.objects.create(envia=self.envia_user, recibe=self.recibe_user)
        data = {"envia": self.envia_user.id, "recibe": self.recibe_user.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Ya has enviado un like a este usuario")

class RespondToLikeTest(APITestCase):
    def setUp(self):
        self.envia_user = Usuario.objects.create(usuario="envia_user")
        self.recibe_user = Usuario.objects.create(usuario="recibe_user")
        self.like = Like.objects.create(envia=self.envia_user, recibe=self.recibe_user)
        self.url = reverse('responder_like')

    def test_respond_to_like_success_accept(self):
        data = {"envia_id": self.envia_user.id, "recibe_id": self.recibe_user.id, "accion": True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.like.refresh_from_db()
        self.assertTrue(self.like.aceptado)
        self.assertTrue(Match.objects.filter(usuario1=self.envia_user, usuario2=self.recibe_user).exists())
        self.assertTrue(ChatPersonal.objects.filter(usuario=self.envia_user, usuario_match=self.recibe_user).exists())

    def test_respond_to_like_success_decline(self):
        data = {"envia_id": self.envia_user.id, "recibe_id": self.recibe_user.id, "accion": False}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(envia=self.envia_user, recibe=self.recibe_user).exists())
        self.assertEqual(response.data['message'], "Like declinado")

    def test_respond_to_like_like_not_found(self):
        data = {"envia_id": 999, "recibe_id": self.recibe_user.id, "accion": True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "No se encontró el like")

    def test_respond_to_like_already_accepted(self):
        self.like.aceptado = True
        self.like.save()
        data = {"envia_id": self.envia_user.id, "recibe_id": self.recibe_user.id, "accion": True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "El match ya fue aceptado anteriormente") 

from enum import Enum
from api.enums.motivos_reporte_ import MotivosReporte

class ReportarUsuarioTest(APITestCase):
    def setUp(self):
        self.user = Usuario.objects.create(usuario="testuser", password="testpassword")
        self.user_reported = Usuario.objects.create(usuario="reporteduser", password="reportedpassword")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.url = reverse('reportar_usuario')

    @patch('chatApp.consumers.NotificationConsumer.send_report_notification')
    def test_reportar_usuario_success(self, mock_send_report_notification):

        fecha_registro_actual = datetime.now().isoformat()

        data = {
            "usuario_reportado_id": self.user_reported.id,
            "motivo": MotivosReporte.SPAM.value,  
            "comentario": "Contenido spam",
            "fechaRegistro": fecha_registro_actual
        }
        print(data)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Reporte registrado")

        report = Reporte.objects.get(usuario_reportado=self.user_reported)
        self.assertIsNotNone(report)
        self.assertEqual(report.usuario_reportado.id, self.user_reported.id)
        self.assertEqual(report.motivo, MotivosReporte.SPAM.value)
        self.assertEqual(report.comentario, "Contenido spam")
        self.assertIsNotNone(report.fechaRegistro)

        mock_send_report_notification.assert_called_once()

    def test_reportar_usuario_invalid_data(self):
        data = {
            "usuario_reportado_id": self.user_reported.id,
            # Falta 'motivo'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VerReportesTest(APITestCase):
    def setUp(self):
        self.user = Usuario.objects.create(usuario="testuser", password="testpassword")
        self.report1 = Reporte.objects.create(usuario_reportado=self.user, motivo="Inappropriate behavior", fechaRegistro=datetime(2023, 1, 1))
        self.report2 = Reporte.objects.create(usuario_reportado=self.user, motivo="Spam", fechaRegistro=datetime(2023, 2, 1))
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.url = reverse('ver_reportes')

    def test_ver_reportes_success(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ver_reportes_with_date_filter_success(self):
        response = self.client.get(self.url, {'fecha_inicio': '2023-01-01', 'fecha_fin': '2023-01-31'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ver_reportes_invalid_date_format(self):
        response = self.client.get(self.url, {'fecha_inicio': '2023/01/01', 'fecha_fin': '2023/01/31'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Formato de fecha incorrecto. Utilice el formato YYYY-MM-DD.')

class VerReportesUsuarioTest(APITestCase):
    def setUp(self):
        self.user = Usuario.objects.create(usuario="testuser", password="testpassword")
        self.report1 = Reporte.objects.create(usuario_reportado=self.user, motivo="Inappropriate behavior")
        self.report2 = Reporte.objects.create(usuario_reportado=self.user, motivo="Spam")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.url = reverse('ver_reportes_usuario', kwargs={'usuario_id': self.user.id})

    def test_ver_reportes_usuario_success(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ver_reportes_usuario_no_reports(self):
        another_user = Usuario.objects.create(usuario="anotheruser", password="anotherpassword")
        url = reverse('ver_reportes_usuario', kwargs={'usuario_id': another_user.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class UsuarioViewSetTest(APITestCase):
    def setUp(self):
        self.user = Usuario.objects.create(usuario="testuser", password=make_password("testpassword"))
        self.url = reverse('usuario-list')

    def test_list_usuarios(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class RegistrarUsuarioTest(APITestCase):
    def setUp(self):
        self.url = reverse('registrarUsuario')

    def test_registrar_usuario_success(self):
        data = {
            "usuario": "newuser",
            "password": "newpassword",
            "nombre": "Nuevo",
            "apellidoPaterno": "Usuario",
            "apellidoMaterno": "Test",
            "edad": 25,
            "ubicacion": "Ciudad",
            "sexo": "M",
            "telefono": "123456789",
            "estado": "Activo",
            "correo": "newuser@example.com",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(usuario="newuser").exists())

    def test_registrar_usuario_invalid_data(self):
        data = {
            "usuario": ""
            # Missing "password"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginUsuarioTest(APITestCase):
    def setUp(self):
        self.user = Usuario.objects.create(usuario="testuser", password=make_password("testpassword"))
        self.url = reverse('loginUsuario')

    def test_login_usuario_success(self):
        data = {
            "usuario": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_usuario_wrong_password(self):
        data = {
            "usuario": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RegistrarAdminTest(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(usuario="adminuser", password=make_password("adminpassword"), tipoUsuario=TipoUsuario.ADMIN.value)
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.url = reverse('registrarAdmin')

    def test_registrar_admin_success(self):
        data = {
            "usuario": "newadmin",
            "password": "newpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(usuario="newadmin", tipoUsuario=TipoUsuario.ADMIN.value).exists())

    def test_registrar_admin_invalid_data(self):
        data = {
            "usuario": ""
            # Missing "password"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginAdministradorTest(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(usuario="adminuser", password=make_password("adminpassword"), tipoUsuario=TipoUsuario.ADMIN.value)
        self.url = reverse('loginAdministrador')

    def test_login_administrador_success(self):
        data = {
            "usuario": "adminuser",
            "password": "adminpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_administrador_wrong_password(self):
        data = {
            "usuario": "adminuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetUsuariosUsuarioTest(APITestCase):
    def setUp(self):
        self.url = reverse('get_usuarios_usuario')
        self.user1 = Usuario.objects.create(usuario="user1", password=make_password("userpassword"), tipoUsuario=TipoUsuario.USUARIO.value)
        self.user2 = Usuario.objects.create(usuario="user2", password=make_password("userpassword"), tipoUsuario=TipoUsuario.USUARIO.value)

    def test_get_usuarios_usuario(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class GetUsuariosAdminTest(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(usuario="adminuser", password=make_password("adminpassword"), tipoUsuario=TipoUsuario.ADMIN.value)
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.url = reverse('get_usuarios_admin')
        self.admin1 = Usuario.objects.create(usuario="admin1", password=make_password("adminpassword"), tipoUsuario=TipoUsuario.ADMIN.value)
        self.admin2 = Usuario.objects.create(usuario="admin2", password=make_password("adminpassword"), tipoUsuario=TipoUsuario.ADMIN.value)

    def test_get_usuarios_admin(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

class BloquearUsuarioTest(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(usuario="adminuser", password=make_password("adminpassword"), tipoUsuario=TipoUsuario.ADMIN.value)
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.user = Usuario.objects.create(usuario="testuser", password=make_password("testpassword"))
        self.url = reverse('bloquear_usuario', kwargs={'usuario_id': self.user.id})

    def test_bloquear_usuario_success(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.estado, EstadoUsuario.BLOQUEADO.value)

    def test_bloquear_usuario_not_found(self):
        url = reverse('bloquear_usuario', kwargs={'usuario_id': 999})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ActualizarUsuarioTest(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create(usuario="adminuser", password=make_password("adminpassword"), tipoUsuario=TipoUsuario.ADMIN.value)
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.user = Usuario.objects.create(usuario="testuser", password=make_password("testpassword"))
        self.url = reverse('actualizar_usuario', kwargs={'pk': self.user.id})

    def test_actualizar_usuario_success(self):
        data = {
            "usuario": "updateduser"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.usuario, "updateduser")

    def test_actualizar_usuario_not_found(self):
        url = reverse('actualizar_usuario', kwargs={'pk': 999})
        data = {
            "usuario": "updateduser"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

