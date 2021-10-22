import math
from Abstract.Expresion import *
from Abstract.Return import *
from enum import Enum


class FuncionNativa(Enum):
    LOG10 = 0
    LOGBAS = 1
    SEN = 2
    COS = 3
    TAN = 4
    RAIZ = 5
    UPPER = 6
    LOWER = 7
    PARSE = 8
    TRUNC = 9
    FLOAT = 10
    STRING = 11
    TYPEOF = 12


class Nativo(Expresion):

    def __init__(self, arg1, arg2, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.arg1 = arg1
        self.arg2 = arg2
        self.tipo = tipo
