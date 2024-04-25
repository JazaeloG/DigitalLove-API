from enum import Enum

class EstadoUsuario(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    BLOQUEADO = "BLOQUEADO"
    ELIMINADO = "ELIMINADO"