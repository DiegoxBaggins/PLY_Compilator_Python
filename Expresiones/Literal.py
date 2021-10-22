from Abstract.Expresion import *
from Abstract.Return import *


class Literal(Expresion):

    def __init__(self, valor, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.valor = valor
        self.tipo = tipo

    def compilar(self, env):
        if self.tipo == Tipo.INT or self.tipo == Tipo.FLOAT:
            return Return(str(self.valor), self.tipo, False)
        else:
            print('Incompleto')
