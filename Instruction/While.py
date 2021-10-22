from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Entorno import *


class While(Expresion):
    def __init__(self, condicion, instrucciones, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones

    def execute(self, entorno):
        condicion = self.condicion.execute(entorno)
        if condicion.tipo != Tipo.BOOLEAN:
            print("La condicion no es bool")
            entorno.guardarError("La condicion no es bool", self.linea, self.columna)
            return
        control = 0
        nuevoEntorno = Entorno(entorno, "WHILE")
        while condicion.valor is True and control < 250:
            rtr = self.instrucciones.execute(nuevoEntorno)
            condicion = self.condicion.execute(entorno)
            control += 1
            if rtr is not None:
                if rtr.tipo == Tipo.BREAKINS:
                    break
                elif rtr.tipo == Tipo.CONTINUEINS:
                    continue
                else:
                    return rtr
        if control == 250:
            print("Error en sentencia While, stack overflow")
            entorno.guardarError("Error en sentencia While, stack overflow", self.linea, self.columna)

    def graph(self, grafo, graph):
        grafo.node(str(graph.indice), "WHILE")
        grafo.edge(str(graph.pivote1), str(graph.indice))
        graph.pivote1 = graph.indice
        graph.indice += 1
        grafo.node(str(graph.indice), "Condición")
        grafo.edge(str(graph.pivote1), str(graph.indice))
        aux = graph.pivote1
        graph.pivote1 = graph.indice
        graph.indice += 1
        self.condicion.graph(grafo, graph)
        graph.indice += 1
        graph.pivote1 = aux
        grafo.node(str(graph.indice), "INSTRUCCIONES")
        grafo.edge(str(aux), str(graph.indice))
        graph.pivote1 = graph.indice
        graph.indice += 1
        self.instrucciones.graph(grafo, graph)
        graph.pivote1 = aux
