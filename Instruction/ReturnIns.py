from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class ReturnIns(Expresion):
    def __init__(self, exp, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.exp = exp

    def compilar(self, entorno):
        if entorno.returnl == '':
            print("Return fuera de funcion")
            return
        genAux = Generador()
        generator = genAux.getInstancia()
        if self.exp is not None:
            valor = self.exp.compilar(entorno)
            if valor.tipo != Tipo.BOOLEAN:
                generator.setStack('P', valor.valor)
            else:
                tempLbl = generator.agregarLabel()

                generator.printLabel(valor.truel)
                generator.setStack('P', '1')
                generator.printGoto(tempLbl)

                generator.printLabel(valor.falsel)
                generator.setStack('P', '0')
                generator.printLabel(tempLbl)
        generator.printGoto(entorno.returnl)
