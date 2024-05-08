from enum import Enum

class ValidacionesReporte(Enum):
    REPORTE_REGISTRADO = 'Reporte registrado exitosamente'
    REPORTE_NO_REGISTRADO = 'Reporte no registrado'

class BloqueoHelper(Enum):
    BLOQUEO_REGISTRADO = 'Bloqueo registrado exitosamente'
    BLOQUEO_NO_REGISTRADO = 'Bloqueo no registrado'
    BLOQUE_REPETIDO = 'El usuario ya se encuentra bloqueado'
