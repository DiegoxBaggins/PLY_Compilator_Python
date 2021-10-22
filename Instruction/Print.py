from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class Print(Expresion):

    def __init__(self, valor, linea, columna, salto=False):
        Expresion.__init__(self, linea, columna)
        self.valor = valor
        self.salto = salto

    def compilar(self, entorno):
        for val in self.valor:
            valor = val.compilar(entorno)
            genAux = Generador()
            generador = genAux.getInstancia()

            if valor.tipo == Tipo.INT:
                generador.agregarPrint("d", valor.valor)
            else:
                print("Incompleto")