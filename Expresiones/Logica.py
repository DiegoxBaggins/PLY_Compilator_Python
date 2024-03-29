from Abstract.Expresion import *
from Abstract.Return import *
from enum import Enum
from Symbol.Generador import *


class OperacionLogica(Enum):
    OR = 0
    AND = 1
    NOT = 2


class Logica(Expresion):

    def __init__(self, izq, der, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.izq = izq
        self.der = der
        self.tipo = tipo

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("INICIO EXPRESION LOGICA")

        self.checkLabels()
        lblAndOr = ''

        if self.tipo == OperacionLogica.AND:
            lblAndOr = self.izq.truel = generador.agregarLabel()
            self.der.truel = self.truel
            self.izq.falsel = self.der.falsel = self.falsel
        elif self.tipo == OperacionLogica.OR:
            self.izq.truel = self.der.truel = self.truel
            lblAndOr = self.izq.falsel = generador.agregarLabel()
            self.der.falsel = self.falsel
        else:
            self.izq.truel = self.falsel
            self.izq.falsel = self.truel
            izq = self.izq.compilar(entorno)
            if izq.tipo != Tipo.BOOLEAN:
                entorno.guardarError("Solo Booleanos adimitidos en logicos", self.linea, self.columna)
                return Return(False, Tipo.BOOLEAN, False)
            generador.agregarCometario("FINALIZO EXPRESION LOGICA")
            generador.agregarEspacio()
            ret = Return(None, Tipo.BOOLEAN, False)
            ret.truel = self.truel
            ret.falsel = self.falsel
            return ret
        izq = self.izq.compilar(entorno)
        if izq.tipo != Tipo.BOOLEAN:
            entorno.guardarError("Solo Booleanos adimitidos en logicos", self.linea, self.columna)
            return Return(False, Tipo.BOOLEAN, False)
        generador.printLabel(lblAndOr)
        der = self.der.compilar(entorno)
        if der.tipo != Tipo.BOOLEAN:
            entorno.guardarError("Solo Booleanos adimitidos en logicos", self.linea, self.columna)
            return Return(False, Tipo.BOOLEAN, False)
        generador.agregarCometario("FINALIZO EXPRESION LOGICA")
        generador.agregarEspacio()
        ret = Return(None, Tipo.BOOLEAN, False)
        ret.truel = self.truel
        ret.falsel = self.falsel
        return ret

    def checkLabels(self):
        genAux = Generador()
        generador = genAux.getInstancia()
        if self.truel == '':
            self.truel = generador.agregarLabel()
        if self.falsel == '':
            self.falsel = generador.agregarLabel()
