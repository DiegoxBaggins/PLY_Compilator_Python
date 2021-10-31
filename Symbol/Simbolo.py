from Abstract.Return import *


class Simbolo:

    def __init__(self, id, tipo, posicion, esGlobal, heap):
        self.valor = None
        self.id = id
        self.tipo = tipo
        self.posicion = posicion
        self.glb = esGlobal
        self.heap = heap
