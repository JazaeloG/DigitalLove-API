from enum import Enum

class ErroresLogin(Enum):
    MENSAJE = 'Credenciales inválidas'
    USUARIO_NO_ENCONTRADO = 'Usuario no encontrado'
    CREDECIALES_INCOMPLETAS = 'Credenciales incompletas'
    USUARIO_NO_ADMIN = 'El usuario no es administrador'
    CUENTA_BLOQUEADA = 'Esta cuenta esta bloqueada. Por favor, contacta al soporte para obtener ayuda.'
    CUENTA_ELIMINADA = 'Esta cuenta ha sido eliminada. Por favor, contacta al soporte para obtener ayuda.'

class ExitoLogin(Enum):
    MENSAJE = 'Usuario autenticado'
    CODIGO = 200