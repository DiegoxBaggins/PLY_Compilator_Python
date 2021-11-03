from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Entorno import *


class Sentencia(Expresion):

    def __init__(self, instrucciones, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.instrucciones = instrucciones

    def compilar(self, entorno):
        for instruccion in self.instrucciones:
            ret = instruccion.compilar(entorno)
            if ret is not None:
                return ret