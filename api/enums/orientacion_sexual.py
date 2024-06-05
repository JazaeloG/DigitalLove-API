from enum import Enum

class OrientacionSexual(Enum):
    HETEROSEXUAL = 'HETEROSEXUAL'
    HOMOSEXUAL = 'HOMOSEXUAL'
    BISEXUAL = 'BISEXUAL'
    OTRO = 'OTRO'

class SexoPreferido(Enum):
    MASCULINO = 'MASCULINO'
    FEMENINO = 'FEMENINO'
    AMBOS = 'AMBOS'