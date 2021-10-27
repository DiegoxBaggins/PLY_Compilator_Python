from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class Literal(Expresion):

    def __init__(self, valor, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.valor = valor
        self.tipo = tipo

    def compilar(self, env):
        if self.tipo == Tipo.INT or self.tipo == Tipo.FLOAT:
            return Return(str(self.valor), self.tipo, False)
        elif self.tipo == Tipo.BOOLEAN:
            genAux = Generador()
            generador = genAux.getInstancia()
            if self.truel == '':
                self.truel = generador.agregarLabel()
            if self.falsel == '':
                self.falsel = generador.agregarLabel()

            if self.valor:
                generador.printGoto(self.truel)
                generador.agregarCometario("GOTO para evitar errores en go")
                generador.printGoto(self.falsel)
            else:
                generador.printGoto(self.falsel)
                generador.agregarCometario("GOTO para evitar errores en go")
                generador.printGoto(self.truel)

            ret = Return(self.valor, self.tipo, False)
            ret.truel = self.truel
            ret.falsel = self.falsel
            return ret
        else:
            print('Incompleto')
