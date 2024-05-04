from enum import Enum

class ErroresToken(Enum):
    AUTH_TOKEN_NOT_FOUND = 'Token de autenticación no encontrado'
    AUTH_TOKEN_INVALID = 'Token de autenticación inválido'
    AUTH_TOKEN_EXPIRED = 'Token de autenticación expirado'
    AUTH_TOKEN_MALFORMED = 'Token de autenticación malformado'