from Abstract.Expresion import *
from Abstract.Return import *
from enum import Enum
from Symbol.Simbolo import Simbolo
from Symbol.Generador import *


class TipoAcceso(Enum):
    GLOBAL = 0
    LOCAL = 1
    VACIO = 2


class Declaracion(Expresion):
    def __init__(self, acceso, id, valor, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.acceso = acceso
        self.id = id
        self.valor = valor
        self.tipo = tipo

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("Compilacion de valor de variable")
        # Compilacion de valor que estamos asignando
        valor = self.valor.compilar(entorno)

        generador.agregarCometario("Fin de valor de variable")

        # Guardado y obtencion de variable. Esta tiene la posicion, lo que nos sirve para asignarlo en el heap
        newVar = entorno.guardarVar(self.id, valor.tipo, (valor.tipo == Tipo.STRING or valor.tipo == Tipo.STRUCT))

        # Obtencion de posicion de la variable
        tempPos = newVar.posicion
        if not newVar.glb:
            tempPos = generador.agregarTemp()
            generador.agregarExp(tempPos, 'P', newVar.posicion, "+")

        if valor.tipo == Tipo.BOOLEAN:
            tempLbl = generador.agregarLabel()

            generador.printLabel(valor.truel)
            generador.setStack(tempPos, "1")

            generador.printGoto(tempLbl)

            generador.printLabel(valor.falsel)
            generador.setStack(tempPos, "0")

            generador.printLabel(tempLbl)
        else:
            generador.setStack(tempPos, valor.valor)
        generador.agregarEspacio()
