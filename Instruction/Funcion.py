from Abstract.Expresion import *


class Function(Expresion):
    def __init__(self, id, params, instr, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.params = params
        self.instrucciones = instr
