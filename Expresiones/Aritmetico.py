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
        validar1 = valorIzq.tipo == Tipo.INT or valorIzq.tipo == Tipo.FLOAT
        validar2 = valorDer.tipo == Tipo.INT or valorDer.tipo == Tipo.FLOAT
        if validar1 and validar2:
            if self.tipo == OperacionAritmetica.SUMA:
                op = '+'
                generador.agregarExp(temp, valorIzq.valor, valorDer.valor, op)
            elif self.tipo == OperacionAritmetica.RESTA:
                op = '-'
                generador.agregarExp(temp, valorIzq.valor, valorDer.valor, op)
            elif self.tipo == OperacionAritmetica.MULTI:
                op = '*'
                generador.agregarExp(temp, valorIzq.valor, valorDer.valor, op)
            elif self.tipo == OperacionAritmetica.DIV:
                op = '/'
                generador.agregarExp(temp, valorIzq.valor, valorDer.valor, op)
            elif self.tipo == OperacionAritmetica.MENOS:
                op = "-"
                generador.agregarExp(temp, '', valorDer.valor, op)
            elif self.tipo == OperacionAritmetica.MODULO:
                generador.agregarMod(temp, valorIzq.valor, valorDer.valor)
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
        if valorIzq.tipo == Tipo.STRING and valorDer.tipo == Tipo.STRING:
            if self.tipo == OperacionAritmetica.MULTI:
                print("concatenacion")
                generador.concatenarStr()

                paramTemp = generador.agregarTemp()

                generador.agregarExp(paramTemp, "P", entorno.tamano, "+")
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, valorIzq.valor)
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, valorDer.valor)

                generador.nuevoEnt(entorno.tamano)
                generador.llamarFun("concatenar")

                generador.getStack(temp, 'P')
                generador.regresarEnt(entorno.tamano)
                return Return(temp, Tipo.STRING, True)
            else:
                print("error")
        if valorIzq.tipo == Tipo.STRING and valorDer.tipo == Tipo.INT:
            if self.tipo == OperacionAritmetica.POTENCIA:
                print("concatenacion")
                generador.multiplicarStr()

                paramTemp = generador.agregarTemp()

                generador.agregarExp(paramTemp, "P", entorno.tamano, "+")
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, valorIzq.valor)
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, valorDer.valor)

                generador.nuevoEnt(entorno.tamano)
                generador.llamarFun("multStr")

                generador.getStack(temp, 'P')
                generador.regresarEnt(entorno.tamano)
                return Return(temp, Tipo.STRING, True)
            else:
                print("error")
