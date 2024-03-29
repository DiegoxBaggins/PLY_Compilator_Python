from Abstract.Expresion import *
from Abstract.Return import *
from enum import Enum
from Symbol.Generador import *


class OperacionRelacional(Enum):
    MAYOR = 0
    MENOR = 1
    MAYORIGUAL = 2
    MENORIGUAL = 3
    IGUALES = 4
    DISTINTOS = 5


class Relacional(Expresion):

    def __init__(self, izq, der, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.izq = izq
        self.der = der
        self.tipo = tipo

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("INICIO EXPRESION RELACIONAL")

        izq = self.izq.compilar(entorno)
        der = None

        resultado = Return(None, Tipo.BOOLEAN, False)

        if izq.tipo != Tipo.BOOLEAN:
            der = self.der.compilar(entorno)
            if (izq.tipo == Tipo.INT or izq.tipo == Tipo.FLOAT) and (der.tipo == Tipo.INT or der.tipo == Tipo.FLOAT):
                self.checkLabels()
                generador.agregarIf(izq.valor, der.valor, self.getOp(), self.truel)
                generador.printGoto(self.falsel)  # ELSE
            elif izq.tipo == Tipo.STRING and der.tipo == Tipo.STRING:
                self.checkLabels()
                temp = generador.agregarTemp()
                generador.compararStr()

                paramTemp = generador.agregarTemp()

                generador.agregarExp(paramTemp, "P", entorno.tamano, "+")
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, izq.valor)
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, der.valor)

                generador.nuevoEnt(entorno.tamano)
                generador.llamarFun("cmpStr")

                generador.getStack(temp, 'P')
                generador.regresarEnt(entorno.tamano)

                if self.tipo == OperacionRelacional.IGUALES:
                    generador.agregarIf(temp, '1', '==', self.truel)
                    generador.printGoto(self.falsel)
                if self.tipo == OperacionRelacional.DISTINTOS:
                    generador.agregarIf(temp, '1', '==', self.falsel)
                    generador.printGoto(self.truel)

        else:
            irDerecha = generador.agregarLabel()
            izqTemp = generador.agregarTemp()

            generador.printLabel(izq.truel)
            generador.agregarExp(izqTemp, '1', '', '')
            generador.printGoto(irDerecha)

            generador.printLabel(izq.falsel)
            generador.agregarExp(izqTemp, '0', '', '')

            generador.printLabel(irDerecha)

            der = self.der.compilar(entorno)
            if der.tipo != Tipo.BOOLEAN:
                entorno.guardarError("No se pueden comparar tipos", self.linea, self.columna)
                return Return(False, Tipo.BOOLEAN, False)
            irFinal = generador.agregarLabel()
            dertemp = generador.agregarTemp()

            generador.printLabel(der.truel)

            generador.agregarExp(dertemp, '1', '', '')
            generador.printGoto(irFinal)

            generador.printLabel(der.falsel)
            generador.agregarExp(dertemp, '0', '', '')

            generador.printLabel(irFinal)

            self.checkLabels()
            generador.agregarIf(izqTemp, dertemp, self.getOp(), self.truel)
            generador.printGoto(self.falsel)

        generador.agregarCometario("FIN DE EXPRESION RELACIONAL")
        generador.agregarEspacio()
        resultado.truel = self.truel
        resultado.falsel = self.falsel

        return resultado

    def checkLabels(self):
        genAux = Generador()
        generador = genAux.getInstancia()
        if self.truel == '':
            self.truel = generador.agregarLabel()
        if self.falsel == '':
            self.falsel = generador.agregarLabel()

    def getOp(self):
        if self.tipo == OperacionRelacional.MAYOR:
            return '>'
        elif self.tipo == OperacionRelacional.MENOR:
            return '<'
        elif self.tipo == OperacionRelacional.MENORIGUAL:
            return '<='
        elif self.tipo == OperacionRelacional.MAYORIGUAL:
            return '>='
        elif self.tipo == OperacionRelacional.IGUALES:
            return '=='
        elif self.tipo == OperacionRelacional.DISTINTOS:
            return '!='
