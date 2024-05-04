from enum import Enum

class ExitoRegistro(Enum):
    REGISTRO_EXITOSO = 'Registro exitoso'
    CODIGO = 201


class ErroresRegistro(Enum):
    MENSAJE = 'Error al registrar usuario'
    USUARIO_YA_EXISTE = 'Este usuario ya existe'
    FORMATO_TELEFONO = 'Formato de teléfono inválido'
    FORMATO_EMAIL = 'Formato de correo inválido'
    FORMATO_PASSWORD = 'Formato de contraseña inválido'
    FORMATO_EDAD = 'Formato de edad inválido'
    FORMATO_GENERO = 'Formato de género inválido'
    FORMATO_NOMBRE = 'Formato de nombre inválido'
    FORMATO_APELLIDO_PATERNO = 'Formato de apellido paterno inválido'
    FORMATO_APELLIDO_MATERNO = 'Formato de apellido materno inválido'
    FORMATO_UBICACION = 'Formato de ubicación inválido'


