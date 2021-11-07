from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Generador import *


class Literal(Expresion):

    def __init__(self, valor, tipo, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.valor = valor
        self.tipo = tipo

    def compilar(self, env):
        genAux = Generador()
        generador = genAux.getInstancia()
        if self.tipo == Tipo.INT or self.tipo == Tipo.FLOAT:
            return Return(str(self.valor), self.tipo, False)
        elif self.tipo == Tipo.BOOLEAN:
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
        elif self.tipo == Tipo.STRING:
            retTemp = generador.agregarTemp()
            generador.agregarExp(retTemp, 'H', '', '')

            for char in str(self.valor):
                generador.setHeap('H', ord(char))  # heap[H] = NUM;
                generador.nextHeap()  # H = H + 1;

            generador.setHeap('H', '-1')  # FIN DE CADENA
            generador.nextHeap()

            return Return(retTemp, Tipo.STRING, True)
        elif self.tipo == Tipo.CHAR:
            return Return(ord(self.valor), self.tipo, False)
        else:
            print('Incompleto')
