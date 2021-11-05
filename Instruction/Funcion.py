from Abstract.Expresion import *
from Symbol.Generador import *


class Funcion(Expresion):
    def __init__(self, id, params, instr, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.params = params
        self.instrucciones = instr
        self.tipo = tipo

    def compilar(self, entorno):
        func = entorno.getFunc(self.id)
        if func is None:
            entorno.newFunc(self.id, self)
            entorno.guardarTS(self.id, self.linea, self.columna, "Funcion")

            genAux = Generador()
            generador = genAux.getInstancia()

            newEnv = Entorno(entorno, self.id)

            returnl = generador.agregarLabel()
            newEnv.returnl = returnl
            newEnv.tamano = 1

            for param in self.params:
                newEnv.guardarVarLocal(param.id, param.tipo, (param.tipo == Tipo.STRING or param.tipo == Tipo.STRUCT),
                                       self.linea, self.columna)

            generador.abrirFun(self.id)

            self.instrucciones.compilar(newEnv)

            generador.printLabel(returnl)
            generador.cerrarFun()
        else:
            print("Funcion " + self.id + "repetida")
            entorno.guardarError("Funcion " + self.id + "repetida", self.linea, self.columna)
