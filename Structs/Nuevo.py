from Abstract.Expresion import *
from enum import Enum


class TipoStruct(Enum):
    NOMUTABLE = 0
    MUTABLE = 1


class NuevoStruct(Expresion):
    def __init__(self, tipo, id, atributos, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.tipo = tipo
        self.id = id
        self.atributos = atributos
