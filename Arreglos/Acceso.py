from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class AccesoArreglo(Expresion):
    def __init__(self, id, exp, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.exp = exp

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("Compilacion de Acceso a Arreglo")

        recibe = entorno.getVar(self.id)

        if recibe is None:
            print("Error, no existe la variable")
            return
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

        tempValor = self.exp.compilar(entorno)
        tempTamano = generador.agregarTemp()
        generador.getHeap(tempTamano, apuntadorStack)

        verdadero = generador.agregarLabel()
        salir = generador.agregarLabel()
        generador.agregarIf(tempTamano, tempValor.valor, '<', verdadero)

        generador.agregarExp(apuntadorStack, apuntadorStack, tempValor.valor, '+')

        tempRetorno = generador.agregarTemp()
        generador.getHeap(tempRetorno, apuntadorStack)

        generador.printGoto(salir)
        generador.printLabel(verdadero)
        generador.printOutBounds()
        generador.llamarFun("outOfBounds")
        generador.agregarExp(tempRetorno, 'H', '', '')
        generador.setHeap('H', '0')
        generador.nextHeap()
        generador.setHeap('H', '-1')
        generador.nextHeap()
        generador.printLabel(salir)



        generador.agregarCometario("Fin compilacion acceso")
        generador.agregarEspacio()
        return Return(tempRetorno, var.auxTipo, True)


