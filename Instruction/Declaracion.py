from Abstract.Expresion import *
from Abstract.Return import *
from enum import Enum
from Symbol.Simbolo import Simbolo


class TipoAcceso(Enum):
    GLOBAL = 0
    LOCAL = 1
    VACIO = 2


class Declaracion(Expresion):
    def __init__(self, acceso, id, valor, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.acceso = acceso
        self.id = id
        self.valor = valor
        self.tipo = tipo
