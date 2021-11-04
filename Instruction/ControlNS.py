from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


def comprobarEntorno(entorno):
    env = entorno
    while env is not None:
        if env.nombre == "FOR" or env.nombre == "WHILE":
            return True
        else:
            env = env.prev
    return False


class ControlIns(Expresion):
    def __init__(self, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.tipo = tipo

    def compilar(self, entorno):
        if comprobarEntorno(entorno):
            genAux = Generador()
            generador = genAux.getInstancia()
            if self.tipo == Tipo.BREAKINS:
                generador.printGoto(entorno.breakl)
            elif self.tipo == Tipo.CONTINUEINS:
                generador.printGoto(entorno.continuel)
            elif self.tipo == Tipo.RETURNINS:
                generador.printGoto(entorno.returnl)
        else:
            "Fuera de ciclo"
            return
