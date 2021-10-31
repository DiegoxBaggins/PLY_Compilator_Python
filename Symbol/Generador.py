from .Entorno import Entorno
from Abstract.Return import *


class Generador:
    generador = None

    def __init__(self):
        # Contadores
        self.totTemp = 0
        self.totLabel = 0
        # Code
        self.codigo = ''
        self.funcs = ''
        self.nativas = ''
        self.enFunc = False
        self.enNativa = False
        # Lista de Temporales
        self.temps = []
        # Lista de Nativas
        self.printString = False

    def limpiarTodo(self):
        # Contadores
        self.totTemp = 0
        self.totLabel = 0
        self.codigo = ''
        self.funcs = ''
        self.nativas = ''
        self.enFunc = False
        self.enNativa = False
        # Lista de Temporales
        self.temps = []
        # Lista de Nativas
        self.printString = False
        Generador.generador = None

    # CODIGO
    def agregarCodigo(self, codigo, tab="\t"):
        if self.enNativa:
            if self.nativas == '':
                self.nativas = '/*-----NATIVES-----*/\n'
            self.nativas += tab + codigo
        elif self.enFunc:
            if self.funcs == '':
                self.funcs = '/*-----FUNCS-----*/\n'
            self.funcs += tab + codigo
        else:
            self.codigo += '\t' + codigo

    def agregarCometario(self, comentario):
        self.agregarCodigo(f'/* {comentario} */\n')

    def getInstancia(self):
        if Generador.generador is None:
            Generador.generador = Generador()
        return Generador.generador

    def getCabeza(self):
        codigo = "package main \nimport (\n\t\"fmt\"\n)\n\n"
        if len(self.temps) > 0:
            codigo += "var "
            temporales = ""
            for temp in self.temps:
                temporales += temp + ", "
            codigo += temporales[:len(temporales) - 2]
            codigo += " float64;\n\n"
        codigo += "var P, H float64;\nvar stack [26102009]float64;\nvar heap [26102009]float64;\n\n"
        return codigo

    def getCodigo(self):
        codigo = self. getCabeza()
        codigo += self.nativas + "\n"
        codigo += self.funcs + "\n"
        codigo += "func main() {\n"
        codigo += self.codigo + "\n"
        codigo += "}"
        return codigo

    def agregarEspacio(self):
        self.agregarCodigo("\n")

    # Manejo de Temporales
    def agregarTemp(self):
        temp = f't{self.totTemp}'
        self.totTemp += 1
        self.temps.append(temp)
        return temp

    # EXPRESIONES
    def agregarExp(self, resultado, izq, der, op):
        self.agregarCodigo(f'{resultado}={izq}{op}{der};\n')

    # LABELS
    def agregarLabel(self):
        label = f'L{self.totLabel}'
        self.totLabel += 1
        return label

    def printLabel(self, label):
        self.agregarCodigo(f'{label}:\n')

    # GOTO
    def printGoto(self, label):
        self.agregarCodigo(f'goto {label};\n')

    # INSTRUCCIONES
    def agregarPrint(self, tipo, valor):
        if tipo != "f":
            self.agregarCodigo(f'fmt.Printf("%{tipo}", int({valor}));\n')
        else:
            self.agregarCodigo(f'fmt.Printf("%{tipo}", {valor});\n')

    # IF
    def agregarIf(self, left, right, op, label):
        self.agregarCodigo(f'if {left} {op} {right} {{goto {label};}}\n')

    # FUNCIONES
    def abrirFun(self, id):
        if not self.enNativa:
            self.enFunc = True
        self.agregarCodigo(f'func {id}(){{\n', '')

    def cerrarFun(self):
        self.agregarCodigo('return;\n}\n')
        if not self.enNativa:
            self.enFunc = False

    # STACK
    def setStack(self, pos, valor):
        self.agregarCodigo(f'stack[int({pos})]={valor};\n')

    def getStack(self, var, pos):
        self.agregarCodigo(f'{var}=stack[int({pos})];\n')

    # ENTORNOS
    def nuevoEnt(self, tamano):
        self.agregarCodigo(f'P=P+{tamano};\n')

    def llamarFun(self, id):
        self.agregarCodigo(f'{id}();\n')

    def regresarEnt(self, tamano):
        self.agregarCodigo(f'P=P-{tamano};\n')

    # HEAP
    def setHeap(self, pos, valor):
        self.agregarCodigo(f'heap[int({pos})]={valor};\n')

    def getHeap(self, var, pos):
        self.agregarCodigo(f'{var}=heap[int({pos})];\n')

    def nextHeap(self):
        self.agregarCodigo('H=H+1;\n')

    #TRUE-FALSE
    def printTrue(self):
        self.agregarPrint("c", 116)
        self.agregarPrint("c", 114)
        self.agregarPrint("c", 117)
        self.agregarPrint("c", 101)

    def printFalse(self):
        self.agregarPrint("c", 102)
        self.agregarPrint("c", 97)
        self.agregarPrint("c", 108)
        self.agregarPrint("c", 115)
        self.agregarPrint("c", 101)

    # NATIVAS
    def printStr(self):
        if self.printString:
            return
        self.printString = True
        self.inNatives = True

        self.abrirFun('printString')
        # Label para salir de la funcion
        final = self.agregarLabel()
        # Label para la comparacion para buscar fin de cadena
        comparar = self.agregarLabel()

        # Temporal puntero a Stack
        tempP = self.agregarTemp()

        # Temporal puntero a Heap
        tempH = self.agregarTemp()

        self.agregarExp(tempP, 'P', '1', '+')

        self.getStack(tempH, tempP)

        # Temporal para comparar
        tempC = self.agregarTemp()

        self.printLabel(comparar)

        self.getHeap(tempC, tempH)

        self.agregarIf(tempC, '-1', '==', final)

        self.agregarPrint('c', tempC)

        self.agregarExp(tempH, tempH, '1', '+')

        self.printGoto(comparar)

        self.printLabel(final)
        self.cerrarFun()
        self.enNativa = False
