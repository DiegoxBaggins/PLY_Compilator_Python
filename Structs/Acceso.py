from Abstract.Expresion import *


class AccesoStruct(Expresion):
    def __init__(self, id, atributo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.atributo = atributo
