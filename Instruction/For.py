from Abstract.Expresion import *
from Abstract.Return import *
from Expresiones.Acceso import Acceso
from Expresiones.Aritmetico import Aritmetico, OperacionAritmetica
from Expresiones.Literal import Literal
from Instruction.Declaracion import Declaracion, TipoAcceso
from Symbol.Entorno import *
from Symbol.Generador import *


class For(Expresion):
    def __init__(self, variable, exp1, exp2, instrucciones, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.variable = variable
        self.exp1 = exp1
        self.exp2 = exp2
        self.instrucciones = instrucciones

    def compilar(self, entorno):
        genAux = Generador()
        generador = genAux.getInstancia()
        idVar = self.variable
        nuevoEntorno = Entorno(entorno, "FOR")
        if self.exp2 is not None:
            continuel = generador.agregarLabel()
            breakl = generador.agregarLabel()
            nuevoEntorno.breakl = breakl
            nuevoEntorno.continuel = continuel
            generador.agregarCometario("INICION FOR")
            declaracion = Declaracion(TipoAcceso.LOCAL, idVar, self.exp1, Tipo.INT, self.linea, self.columna)
            declaracion.compilar(nuevoEntorno)
            expresion2 = self.exp2.compilar(entorno)

            generador.printLabel(continuel)
            consulta = Acceso(idVar, self.linea, self.columna)
            variable = consulta.compilar(nuevoEntorno)

            generador.agregarIf(variable.valor, expresion2.valor, '>', breakl)
            self.instrucciones.compilar(nuevoEntorno)
            # variable = consulta.compilar(nuevoEntorno)
            # generador.agregarExp(variable.valor, variable.valor, '1', '+')
            aritmetica = Aritmetico(consulta, Literal(1, Tipo.INT, self.linea, self.columna), OperacionAritmetica.SUMA, self.linea, self.columna)
            actualizacion = Declaracion(TipoAcceso.LOCAL, idVar, aritmetica, Tipo.INT, self.linea, self.columna)
            actualizacion.compilar(nuevoEntorno)
            # generador.setStack()
            generador.printGoto(continuel)
            generador.printLabel(breakl)
            generador.agregarCometario("FIN FOR")
        else:
            expresion1 = self.exp1.compilar(entorno)
            if expresion1.tipo == Tipo.STRING:
                apuntadorString = generador.agregarTemp()
                continuel = generador.agregarLabel()
                breakl = generador.agregarLabel()
                nuevoEntorno.breakl = breakl
                nuevoEntorno.continuel = continuel
                generador.agregarCometario("INICION FOR")
                generador.agregarExp(apuntadorString, expresion1.valor, '', '')

                generador.printLabel(continuel)
                char = generador.agregarTemp()
                generador.getHeap(char, apuntadorString)
                generador.agregarIf(char, '-1', '==', breakl)

                apuntadorHeap = generador.agregarTemp()
                generador.agregarExp(apuntadorHeap, 'H', '', '')
                generador.setHeap('H',  char)  # heap[H] = NUM;
                generador.nextHeap()
                generador.setHeap('H', '-1')  # FIN DE CADENA
                generador.nextHeap()

                newVar = nuevoEntorno.guardarVarLocal(idVar, Tipo.STRING, True, self.linea, self.columna)
                tamano = newVar[1]
                posicion = newVar[2]
                tamano += posicion
                posicion = generador.agregarTemp()
                generador.agregarExp(posicion, 'P', tamano, "+")
                generador.setStack(posicion, apuntadorHeap)
                generador.agregarEspacio()

                self.instrucciones.compilar(nuevoEntorno)
                generador.agregarExp( apuntadorString,  apuntadorString, '1', '+')
                generador.printGoto(continuel)
                generador.printLabel(breakl)
                generador.agregarCometario("FIN FOR")
            elif expresion1.tipo == Tipo.ARRAY:
                print("soy array")
            else:
                print("No se puede hacer For de tipo: " + expresion1.tipo.name)
                entorno.guardarError("No se puede hacer For de tipo: " + expresion1.tipo.name, self.linea, self.columna)

