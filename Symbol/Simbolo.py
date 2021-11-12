from Abstract.Return import *


class Simbolo:

    def __init__(self, id, tipo, posicion, esGlobal, heap, auxTipo=""):
        self.valor = None
        self.id = id
        self.tipo = tipo
        self.auxTipo = auxTipo
        self.posicion = posicion
        self.glb = esGlobal
        self.heap = heap
