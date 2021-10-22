from Abstract.Return import *


class Simbolo:

    def __init__(self, valor, id, tipo, objeto=""):
        self.valor = valor
        self.id = id
        self.tipo = tipo
        self.objeto = objeto
        self.atributos = {}
