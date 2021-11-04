from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Entorno import *
from Symbol.Generador import *


class While(Expresion):
    def __init__(self, condicion, instrucciones, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        continuel = generador.agregarLabel()
        generador.printLabel(continuel)

        condicion = self.condicion.compilar(entorno)
        newEnv = Entorno(entorno, "WHILE")

        newEnv.breakl = condicion.falsel
        newEnv.continuel = continuel

        generador.printLabel(condicion.truel)

        self.instrucciones.compilar(newEnv)
        generador.printGoto(continuel)

        generador.printLabel(condicion.falsel)

