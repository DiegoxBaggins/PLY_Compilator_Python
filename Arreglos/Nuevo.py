from Abstract.Expresion import *
from Abstract.Return import *
from Instruction.Print import *
from Symbol.Generador import *


class NuevoArray(Expresion):
    def __init__(self, expresiones, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.expresiones = expresiones

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()

        generador.agregarCometario("NUEVO ARRAY")
        tamano = len(self.expresiones) + 1
        tempRetorno = generador.agregarTemp()
        tempApuntador = generador.agregarTemp()
        tempCompilacion = generador.agregarTemp()

        generador.agregarExp(tempRetorno, 'H', '', '')
        generador.agregarExp(tempApuntador, 'H', '', '')
        generador.setHeap(tempApuntador, str(tamano-1))
        generador.agregarExp(tempApuntador, tempApuntador, '1', '+')
        generador.agregarExp('H', 'H', str(tamano), '+')

        for expresion in self.expresiones:
            tempCompilacion = expresion.compilar(entorno)
            generador.setHeap(tempApuntador, tempCompilacion.valor)
            generador.agregarExp(tempApuntador, tempApuntador, '1', '+')

        generador.agregarCometario("Fin Nuevo Array")
        return Return(tempRetorno, Tipo.ARRAY, True)


