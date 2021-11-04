from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class Acceso(Expresion):
    def __init__(self, id, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("Compilacion de Acceso")

        var = entorno.getVar(self.id)
        if var is None:
            print("Error, no existe la variable")
            return

        # Temporal para guardar variable
        temp = generador.agregarTemp()

        # Obtencion de posicion de la variable
        tempPos = var.posicion
        if not var.glb:
            tempPos = generador.agregarTemp()
            generador.agregarExp(tempPos, 'P', var.posicion, "+")
        generador.getStack(temp, tempPos)

        if var.tipo != Tipo.BOOLEAN:
            generador.agregarCometario("Fin compilacion acceso")
            generador.agregarEspacio()
            return Return(temp, var.tipo, True)

        if self.truel == '':
            self.truel = generador.agregarLabel()
        if self.falsel == '':
            self.falsel = generador.agregarLabel()

        generador.agregarIf(temp, '1', '==', self.truel)
        generador.printGoto(self.falsel)

        generador.agregarCometario("Fin compilacion acceso")
        generador.agregarEspacio()

        ret = Return(None, Tipo.BOOLEAN, False)
        ret.truel = self.truel
        ret.falsel = self.falsel
        return ret
