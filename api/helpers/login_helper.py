from enum import Enum

class ErroresLogin(Enum):
    MENSAJE = 'Credenciales inválidas'
    USUARIO_NO_ENCONTRADO = 'Usuario no encontrado'
    CREDECIALES_INCOMPLETAS = 'Credenciales incompletas'

class ExitoLogin(Enum):
    MENSAJE = 'Usuario autenticado'
    CODIGO = 200