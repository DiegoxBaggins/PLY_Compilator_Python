from Abstract.Expresion import *
from Abstract.Return import *
from Instruction.Print import *


class NuevoArray(Expresion):
    def __init__(self, expresiones, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.expresiones = expresiones
