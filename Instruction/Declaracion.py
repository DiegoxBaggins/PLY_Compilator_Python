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

    def chequearTipo(self, valor):
        if self.tipo == Tipo.UNDEFINED:
            return True
        else:
            if valor.tipo != self.tipo:
                print(valor.tipo, self.tipo)
                return False
            else:
                return True

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("Compilacion de valor de variable")
        # Compilacion de valor que estamos asignando
        if self.valor is not None:
            valor = self.valor.compilar(entorno)
        else:
            valor = Return(-1, Tipo.NULL, False)

        generador.agregarCometario("Fin de valor de variable")
        if not self.chequearTipo(valor):
            print("error de tipos")
            return

        newVar = None
        posicion = 0
        if self.acceso == TipoAcceso.GLOBAL and self.valor is None:
            entorno.moverGlobal(self.id)
            return
        elif self.acceso == TipoAcceso.GLOBAL:
            newVar = entorno.guardarVarGlobal(self.id, valor.tipo, (valor.tipo == Tipo.STRING
                                                                      or valor.tipo == Tipo.STRUCT), self.linea,
                                                self.columna)

        elif self.acceso == TipoAcceso.LOCAL:
            newVar = entorno.guardarVarLocal(self.id, valor.tipo, (valor.tipo == Tipo.STRING
                                                                     or valor.tipo == Tipo.STRUCT), self.linea,
                                               self.columna)
        else:
            newVar = entorno.guardarVar(self.id, valor.tipo, (valor.tipo == Tipo.STRING
                                                                or valor.tipo == Tipo.STRUCT), self.linea, self.columna)

        var = newVar[0]
        tamano = newVar[1]
        posicion = newVar[2]
        if not var.glb:
            posicion = generador.agregarTemp()
            generador.agregarExp(posicion, 'P', tamano, "+")

        if valor.tipo == Tipo.BOOLEAN:
            tempLbl = generador.agregarLabel()

            generador.printLabel(valor.truel)
            generador.setStack(posicion, "1")

            generador.printGoto(tempLbl)

            generador.printLabel(valor.falsel)
            generador.setStack(posicion, "0")

            generador.printLabel(tempLbl)
        else:
            generador.setStack(posicion, valor.valor)
        generador.agregarEspacio()
