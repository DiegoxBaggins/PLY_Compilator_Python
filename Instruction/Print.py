from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class Print(Expresion):

    def __init__(self, valor, linea, columna, salto=False):
        Expresion.__init__(self, linea, columna)
        self.valor = valor
        self.salto = salto

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        for val in self.valor:
            valor = val.compilar(entorno)
            cuerpo(entorno, generador, valor)

        if self.salto:
            generador.agregarPrint("c", 10)


def cuerpo(entorno, generador, valor):
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
    elif valor.tipo == Tipo.CHAR:
        generador.agregarPrint("c", valor.valor)
    elif valor.tipo == Tipo.ARRAY:
        apuntadorHeap = generador.agregarTemp()
        generador.getHeap(apuntadorHeap, valor.valor)
        tamano = generador.agregarTemp()
        generador.agregarExp(tamano, apuntadorHeap, '', '')
        contador = generador.agregarTemp()
        continuel = generador.agregarLabel()
        breakl = generador.agregarLabel()

        generador.agregarExp(apuntadorHeap, valor.valor, '1', '+')
        generador.agregarExp(contador, '0', '', '')
        generador.printLabel(continuel)

        generador.agregarIf(contador, tamano, '>=', breakl)

        generador.getHeap(valor.valor, apuntadorHeap)
        cuerpo(entorno, generador, Return(valor.valor, valor.auxTipo, True))
        generador.agregarPrint("c", 32)
        generador.agregarExp(apuntadorHeap, apuntadorHeap, '1', '+')
        generador.agregarExp(contador, contador, '1', '+')
        generador.printGoto(continuel)
        generador.printLabel(breakl)
    else:
        print("Incompleto")