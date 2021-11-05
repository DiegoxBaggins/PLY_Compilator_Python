from Abstract.Expresion import *


class Parametro(Expresion):
    def __init__(self, id, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.tipo = tipo

    def compilar(self, entorno):
        return self
