from Abstract.Expresion import *
from Abstract.Return import *
from enum import Enum
from Arreglos.Asignacion import *


class FuncionArreglo(Enum):
    LENGTH = 0
    PUSH = 1
    POP = 2


class FuncArreglo(Expresion):
    def __init__(self, id, exp, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.exp = exp
        self.tipo = tipo

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()
        if self.tipo == FuncionArreglo.LENGTH:
            generador.agregarCometario("Compilacion de Acceso a Arreglo")

            recibe = entorno.getVar(self.id)

            if recibe is None:
                entorno.guardarError("Var no existe", self.linea, self.columna)
                return Return(0, Tipo.INT, False)
            var = recibe[0]
            print(var.auxTipo)
            tamano = recibe[1]
            # Temporal para guardar variable
            apuntadorStack = generador.agregarTemp()

            # Obtencion de posicion de la variable
            tempPos = var.posicion
            if not var.glb:
                tempPos = generador.agregarTemp()
                generador.agregarExp(tempPos, 'P', var.posicion + tamano, "+")
            generador.getStack(apuntadorStack, tempPos)

            tempTamano = generador.agregarTemp()
            generador.getHeap(tempTamano, apuntadorStack)

            generador.agregarCometario("Fin compilacion acceso")
            generador.agregarEspacio()
            return Return(tempTamano, Tipo.INT, True)
