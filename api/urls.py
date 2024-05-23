from django.urls import path, include
from rest_framework import routers
from api.views import user_views, match_views, reporte_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.estadistica_views import obtener_estadisticas
from chatApp.views import notification_views
from chatApp.views import chatList_views
router = routers.DefaultRouter()
router.register(r'usuarios', user_views.UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'registrarUsuario/', user_views.registrarUsuario, name='registrarUsuario'),
    path(r'loginUsuario/', user_views.loginUsuario, name='loginUsuario'),
    path(r'registrarAdmin/', user_views.registrarAdmin, name='registrarAdmin'),
    path(r'loginAdmin/', user_views.loginAdministrador, name='loginAdministrador'),
    path(r'usuariosApp/', user_views.get_usuarios_usuario, name='get_usuarios_usuario'),
    path(r'reportes/', reporte_views.ver_reportes, name='ver_reportes'),
    path(r'reportes/usuario/<int:usuario_id>/', reporte_views.ver_reportes_usuario, name='ver_reportes_usuario'),
    path(r'reportarUsuario/', reporte_views.reportar_usuario, name='reportar_usuario'),
    path(r'bloquearUsuario/<int:usuario_id>/', user_views.bloquear_usuario, name='bloquear_usuario'),
    path(r'usuariosAdmin/', user_views.get_usuarios_admin, name='get_usuarios_admin'),
    path(r'notificaciones/<int:usuario_id>/', notification_views.listar_notificaciones, name='listar_notificaciones'),
    path(r'enviarNotificacion/<int:user_id>/', notification_views.enviar_notificacion, name='enviar_notificacion'),
    path(r'enviarLike/', match_views.like_user, name='like_user'),
    path(r'responder_like/', match_views.respond_to_like, name='responder_like'),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'actualizarUsuario/<int:pk>/', user_views.actualizar_usuario, name='actualizar_usuario'),
    path(r'mensajesAnteriores/<int:chat_personal_id>/', chatList_views.obtener_mensajes_anteriores, name='obtener_mensajes_anteriores'),
    path(r'chatsUsuario/<int:usuario_id>/', chatList_views.get_user_chats, name='get_user_chats'),
    path(r'enviarReporteToAdmin/', notification_views.send_report_to_admin, name='send_report_to_admin'),
    path(r'estadisticas/', obtener_estadisticas, name='obtener_estadisticas'),
]
