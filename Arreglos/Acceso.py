from Abstract.Expresion import *
from Abstract.Return import *


class AccesoArreglo(Expresion):
    def __init__(self, id, exp, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.exp = exp
