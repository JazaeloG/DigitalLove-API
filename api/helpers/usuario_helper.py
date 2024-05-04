from enum import Enum

class ErroresUsuario(Enum):
    USUARIO_NO_ENCONTRADO = 'Usuario no encontrado'
    USUARIO_YA_EXISTE = 'Usuario ya existe'
    USUARIO_NO_ACTUALIZADO = 'Usuario no actualizado'
    USUARIO_NO_ELIMINADO = 'Usuario no eliminado'
    USUARIO_NO_REGISTRADO = 'Usuario no registrado'
    USUARIO_NO_AUTENTICADO = 'Usuario no autenticado'
    USUARIO_NO_AUTORIZADO = 'Usuario no autorizado'
    USUARIO_NO_ACTUALIZADO = 'Usuario no actualizado'
    USUARIO_NO_ELIMINADO = 'Usuario no eliminado'

class ExitoUsuario(Enum):
    USUARIO_REGISTRADO = 'Usuario registrado'
    USUARIO_AUTENTICADO = 'Usuario autenticado'
    USUARIO_ACTUALIZADO = 'Usuario actualizado'
    USUARIO_ELIMINADO = 'Usuario eliminado'