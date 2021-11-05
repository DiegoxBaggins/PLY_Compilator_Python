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
            if valor.tipo == Tipo.INT or valor.tipo == Tipo.FLOAT:
                generador.agregarPrint("f", valor.valor)
            elif valor.tipo == Tipo.BOOLEAN:
                generador.printBolean()
                labelSalir = generador.agregarLabel()

                paramValor = generador.tmpBool
                paramTemp = generador.agregarTemp()

                generador.printLabel(valor.truel)
                generador.agregarExp(paramValor, "1", "", "")

                generador.printGoto(labelSalir)

                generador.printLabel(valor.falsel)
                generador.agregarExp(paramValor, "0", "", "")

                generador.printLabel(labelSalir)

                generador.agregarExp(paramTemp, "P", entorno.tamano, "+")
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, paramValor)
                generador.nuevoEnt(entorno.tamano)
                generador.llamarFun('printBool')

                temp = generador.agregarTemp()
                generador.getStack(temp, 'P')
                generador.regresarEnt(entorno.tamano)

            elif valor.tipo == Tipo.STRING:
                generador.printStr()

                paramTemp = generador.agregarTemp()

                generador.agregarExp(paramTemp, "P", entorno.tamano, "+")
                generador.agregarExp(paramTemp, paramTemp, "1", "+")
                generador.setStack(paramTemp, valor.valor)

                generador.nuevoEnt(entorno.tamano)
                generador.llamarFun('printString')

                temp = generador.agregarTemp()
                generador.getStack(temp, 'P')
                generador.regresarEnt(entorno.tamano)
            else:
                print("Incompleto")

        if self.salto:
            generador.agregarPrint("c", 10)
