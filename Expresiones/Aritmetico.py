from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *
from enum import Enum


class OperacionAritmetica(Enum):
    SUMA = 0
    RESTA = 1
    MULTI = 2
    DIV = 3
    MENOS = 4
    POTENCIA = 6
    MODULO = 7


def casteos(izq, der):
    if izq.tipo == Tipo.FLOAT or der.tipo == Tipo.FLOAT:
        return Return(0.0, Tipo.FLOAT)
    elif izq.tipo == Tipo.STRING or der.tipo == Tipo.STRING:
        return Return("", Tipo.STRING)
    else:
        return Return(0, Tipo.INT)


def comprobar(izq, der):
    if izq.tipo == Tipo.FLOAT or izq.tipo == Tipo.INT:
        if der.tipo == Tipo.FLOAT or der.tipo == Tipo.INT:
            return True
        else:
            return False
    else:
        return False


class Aritmetico(Expresion):

    def __init__(self, izq, der, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.izq = izq
        self.der = der
        self.tipo = tipo

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()
        valorIzq = self.izq.compilar(entorno)
        valorDer = self.der.compilar(entorno)

        temp = generador.agregarTemp()
        op = ''
        if self.tipo == OperacionAritmetica.SUMA:
            op = '+'
        elif self.tipo == OperacionAritmetica.RESTA:
            op = '-'
        elif self.tipo == OperacionAritmetica.MULTI:
            op = '*'
        elif self.tipo == OperacionAritmetica.DIV:
            op = '/'
        elif self.tipo == OperacionAritmetica.MENOS:
            op = "-"
            generador.agregarExp(temp, '', valorDer.valor, op)
            return Return(temp, Tipo.INT, True)
        elif self.tipo == OperacionAritmetica.MODULO:
            generador.agregarMod(temp, valorIzq.valor, valorDer.valor)
            return Return(temp, Tipo.INT, True)
        elif self.tipo == OperacionAritmetica.POTENCIA:
            generador.potencia()

            paramTemp = generador.agregarTemp()

            generador.agregarExp(paramTemp, "P", entorno.tamano, "+")
            generador.agregarExp(paramTemp, paramTemp, "1", "+")
            generador.setStack(paramTemp, valorIzq.valor)
            generador.agregarExp(paramTemp, paramTemp, "1", "+")
            generador.setStack(paramTemp, valorDer.valor)

            generador.nuevoEnt(entorno.tamano)
            generador.llamarFun("doPotencia")

            generador.getStack(temp, 'P')
            generador.regresarEnt(entorno.tamano)
            return Return(temp, Tipo.INT, True)
        generador.agregarExp(temp, valorIzq.valor, valorDer.valor, op)
        return Return(temp, Tipo.INT, True)
