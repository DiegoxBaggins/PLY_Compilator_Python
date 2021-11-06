import math
from Abstract.Expresion import *
from Abstract.Return import *
from enum import Enum
from Symbol.Generador import *


class FuncionNativa(Enum):
    UPPER = 0
    LOWER = 1
    PARSE = 2
    TRUNC = 3
    FLOAT = 4
    STRING = 5


class Nativo(Expresion):

    def __init__(self, arg1, arg2, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.arg1 = arg1
        self.arg2 = arg2
        self.tipo = tipo

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()
        exp = self.arg1.compilar(entorno)
        if self.tipo == FuncionNativa.UPPER or self.tipo == FuncionNativa.LOWER:
            paramTemp = generador.agregarTemp()

            generador.agregarExp(paramTemp, "P", entorno.tamano, "+")
            generador.agregarExp(paramTemp, paramTemp, "1", "+")
            generador.setStack(paramTemp, exp.valor)

            generador.nuevoEnt(entorno.tamano)
            if self.tipo == FuncionNativa.UPPER:
                generador.upper()
                generador.llamarFun("upper")
            if self.tipo == FuncionNativa.LOWER:
                generador.lower()
                generador.llamarFun("lower")

            temp = generador.agregarTemp()
            generador.getStack(temp, 'P')
            generador.regresarEnt(entorno.tamano)
            return Return(temp, Tipo.STRING, True)
