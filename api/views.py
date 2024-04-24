from rest_framework import viewsets
from .serializers import UsuarioSerializer, UsuarioAdministradorSerializer
from api.models import Usuario, UsuarioAdministrador

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioAdministradorViewSet(viewsets.ModelViewSet):
    queryset = UsuarioAdministrador.objects.all()
    serializer_class = UsuarioAdministradorSerializer