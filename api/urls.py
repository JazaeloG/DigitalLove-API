from django.urls import path, include
from rest_framework import routers
from api.views import user_views, match_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'usuarios', user_views.UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'registrarUsuario/', user_views.registrarUsuario),
    path(r'loginUsuario/', user_views.loginUsuario),
    path(r'registrarAdmin/', user_views.registrarAdmin),
    path(r'loginAdmin/', user_views.loginAdministrador),
    path(r'like/', match_views.like_user),
    path(r'respond_to_like/', match_views.respond_to_like),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]