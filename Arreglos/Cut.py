from Abstract.Expresion import *
from Abstract.Return import *
from Arreglos.Asignacion import *


class CutArreglo(Expresion):
    def __init__(self, id, exp1, exp2, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.exp1 = exp1
        self.exp2 = exp2
