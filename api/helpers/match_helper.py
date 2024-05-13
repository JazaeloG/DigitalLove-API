from enum import Enum

class ExitoLike(Enum):
    LIKE_ENVIADO = "Like enviado correctamente"
    MATCH_ACEPTADO = "Match aceptado!"

class ErrorLike(Enum):
    USUARIO_NO_EXISTE = "El usuario recepto no existe"
    LIKE_NO_ENCONTRADO = "No se encontró el like"
    MATCH_YA_ACEPTADO = "El match ya fue aceptado anteriormente"
    LIKE_DECLINADO = "Like declinado"
    LIKE_YA_ENVIADO = "Ya has enviado un like a este usuario"
    NO_CHATS_PERSONALES = "No se encontraron chats personales"
    NO_MENSAJES_CHAT = "No se encontraron mensajes en el chat"