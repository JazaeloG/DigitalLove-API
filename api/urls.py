from django.urls import path, include
from rest_framework import routers
from api.views import user_views, match_views, reporte_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chatApp.views import notification_views
router = routers.DefaultRouter()
router.register(r'usuarios', user_views.UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'registrarUsuario/', user_views.registrarUsuario),
    path(r'loginUsuario/', user_views.loginUsuario),
    path(r'registrarAdmin/', user_views.registrarAdmin),
    path(r'loginAdmin/', user_views.loginAdministrador),
    path(r'usuariosApp/', user_views.get_usuarios_usuario),
    path(r'reportes/', reporte_views.ver_reportes),
    path(r'reportarUsuario/', reporte_views.reportar_usuario),
    path(r'bloquearUsuario/<int:usuario_id>/', user_views.bloquear_usuario),
    path(r'reportesUsuario/<int:usuario_id>/', reporte_views.ver_reportes_usuario),
    path(r'usuariosAdmin/', user_views.get_usuarios_admin),
    path(r'notificaciones/<int:usuario_id>/', notification_views.listar_notificaciones, name='listar_notificaciones'),
    path(r'enviarNotificacion/<int:user_id>/', notification_views.enviar_notificacion, name='enviar_notificacion'),
    path(r'like/', match_views.like_user, name='like_user'),
    path(r'responder_like/', match_views.respond_to_like, name='responder_like'),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]