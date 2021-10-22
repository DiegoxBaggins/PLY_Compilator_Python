from Abstract.Expresion import *
from Abstract.Return import *


class ReturnIns(Expresion):
    def __init__(self, exp, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.exp = exp

    def execute(self, entorno):
        if self.exp is not None:
            valor = self.exp.execute(entorno)
            return valor
        else:
            return Return(None, Tipo.RETURNINS, "")

    def graph(self, grafo, graph):
        if self.exp is not None:
            grafo.node(str(graph.indice), "RETURN")
            grafo.edge(str(graph.pivote1), str(graph.indice))
            graph.pivote1 = graph.indice
            graph.indice += 1
            self.exp.graph(grafo, graph)
        else:
            grafo.node(str(graph.indice), "RETURN")
            grafo.edge(str(graph.pivote1), str(graph.indice))
