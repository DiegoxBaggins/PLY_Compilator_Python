from Abstract.Expresion import *
from Arreglos.Acceso import *
from Abstract.Return import *


class AsignacionArreglo(Expresion):
    def __init__(self, id, exp, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.exp = exp

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("Compilacion de Asignacion a Arreglo")
        acceso = self.id
        varId = acceso.id
        posicion = acceso.exp

        recibe = entorno.getVar(varId)

        if recibe is None:
            print("Error, no existe la variable")
            return
        var = recibe[0]
        tamano = recibe[1]
        # Temporal para guardar variable
        apuntadorStack = generador.agregarTemp()

        # Obtencion de posicion de la variable
        tempPos = var.posicion
        if not var.glb:
            tempPos = generador.agregarTemp()
            generador.agregarExp(tempPos, 'P', var.posicion + tamano, "+")
        generador.getStack(apuntadorStack, tempPos)

        tempPosicionArreglo = posicion.compilar(entorno)
        tempValor = self.exp.compilar(entorno)
        tempTamano = generador.agregarTemp()
        generador.getHeap(tempTamano, apuntadorStack)

        verdadero = generador.agregarLabel()
        salir = generador.agregarLabel()
        generador.agregarIf(tempTamano, tempPosicionArreglo.valor, '<', verdadero)

        generador.agregarExp(apuntadorStack, apuntadorStack, tempPosicionArreglo.valor, '+')

        generador.setHeap(apuntadorStack, tempValor.valor)

        generador.printGoto(salir)
        generador.printLabel(verdadero)
        generador.printOutBounds()
        generador.llamarFun("outOfBounds")
        generador.printLabel(salir)



        generador.agregarCometario("Fin modificiacion")
        generador.agregarEspacio()
