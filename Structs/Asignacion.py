from Abstract.Expresion import *
from Structs.Nuevo import *
from Structs.Acceso import *


class AsignacionStruct(Expresion):
    def __init__(self, id, exp, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.exp = exp
