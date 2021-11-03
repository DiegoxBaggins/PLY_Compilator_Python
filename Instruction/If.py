from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class If(Expresion):

    def __init__(self, condicion, instrucciones, linea, columna, elseIns=None):
        Expresion.__init__(self, linea, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.elseIns = elseIns

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("Compilacion de If")
        condicion = self.condicion.compilar(entorno)

        if condicion.tipo != Tipo.BOOLEAN:
            print('Error, condicion no booleana')
            return

        generador.printLabel(condicion.truel)

        self.instrucciones.compilar(entorno)

        if self.elseIns is not None:
            salirIf = generador.agregarLabel()
            generador.printGoto(salirIf)

        generador.printLabel(condicion.falsel)
        if self.elseIns is not None:
            self.elseIns.compilar(entorno)
            generador.printLabel(salirIf)
