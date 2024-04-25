from django.urls import path, include
from rest_framework import routers
from api.views import user_views

router = routers.DefaultRouter()
router.register(r'usuarios', user_views.UsuarioViewSet)
router.register(r'usuariosAdministradores', user_views.UsuarioAdministradorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'registrarUsuario/', user_views.registrarUsuario),
    path(r'loginUsuario/', user_views.loginUsuario),
    path(r'registrarAdmin/', user_views.registrarAdmin),
    path(r'loginAdmin/', user_views.loginAdministrador),
]