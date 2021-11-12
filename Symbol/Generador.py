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
        self.imports = '\t"fmt"\n'
        self.enFunc = False
        self.enNativa = False
        # Lista de Temporales
        self.temps = []
        # Lista de Nativas
        self.printString = False
        self.printBool = False
        self.tmpBool = self.agregarTemp()
        self.printPotencia = False
        self.mod = False
        self.concatenar = False
        self.multStr = False
        self.compStr = False
        self.funcUpper = False
        self.funcLower = False
        self.mathError = False
        self.outofBounds = False

    def limpiarTodo(self):
        # Contadores
        self.totTemp = 0
        self.totLabel = 0
        self.codigo = ''
        self.funcs = ''
        self.nativas = ''
        self.imports = '\t"fmt"\n'
        self.enFunc = False
        self.enNativa = False
        # Lista de Temporales
        self.temps = []
        # Lista de Nativas
        Generador.generador = None
        self.printString = False
        self.printBool = False
        self.tmpBool = None
        self.printPotencia = False
        self.mod = False
        self.concatenar = False
        self.multStr = False
        self.compStr = False
        self.funcUpper = False
        self.funcLower = False
        self.mathError = False
        self.outofBounds = False

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
        codigo = f"package main \nimport (\n{self.imports})\n\n"
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
        self.agregarCodigo(f'func {id}(){{\n', '')

    def cerrarFun(self):
        self.agregarCodigo('return;\n}\n')

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
        self.enNativa = True

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

    def printBolean(self):
        if self.printBool:
            return
        self.printBool = True
        self.enNativa = True

        self.abrirFun('printBool')
        # Label para salir de la funcion
        final = self.agregarLabel()

        # Temporal puntero a Stack
        tempP = self.agregarTemp()

        valorBool = self.agregarTemp()

        self.agregarExp(tempP, 'P', '1', '+')
        self.getStack(valorBool, tempP)

        truel = self.agregarLabel()
        falsel = self.agregarLabel()

        self.agregarIf(valorBool, '1', '==', truel)
        self.printGoto(falsel)

        self.printLabel(truel)
        self.printTrue()

        self.printGoto(final)

        self.printLabel(falsel)
        self.printFalse()

        self.printLabel(final)
        self.cerrarFun()
        self.enNativa = False

    def potencia(self):
        if self.printPotencia:
            return
        self.printPotencia = True
        self.enNativa = True

        self.abrirFun('doPotencia')
        # Label para salir de la funcion
        final = self.agregarLabel()
        comparar = self.agregarLabel()
        cerrar = self.agregarLabel()

        apuntador = self.agregarTemp()
        # Temporal puntero a base
        tempBase = self.agregarTemp()
        # Temporal puntero a exponente
        tempExp = self.agregarTemp()
        # Temporal puntero a auxiliar
        tempAux = self.agregarTemp()

        self.agregarExp(apuntador, 'P', '1', '+')
        self.getStack(tempBase, apuntador)

        self.agregarExp(apuntador, apuntador, '1', '+')
        self.getStack(tempExp, apuntador)

        self.agregarExp(tempAux, tempBase, '', '')

        self.agregarIf(tempExp, '1', '==', cerrar)

        self.printLabel(comparar)
        self.agregarIf(tempExp, '1', '<=', final)

        self.agregarExp(tempBase, tempBase, tempAux, "*")
        self.agregarExp(tempExp, tempExp, '1', '-')

        self.printGoto(comparar)

        self.printLabel(cerrar)
        self.agregarExp(tempBase, '1', '', '')

        self.printLabel(final)
        self.agregarExp(apuntador, apuntador, '2', '-')
        self.setStack(apuntador, tempBase)
        self.cerrarFun()
        self.enNativa = False

    def agregarMod(self, resultado, izq, der):
        if not self.mod:
            self.mod = True
            self.imports += '\t"math"\n'
        self.agregarCodigo(f'{resultado}=math.Mod({izq},{der});\n')

    def concatenarStr(self):
        if self.concatenar:
            return
        self.concatenar = True
        self.enNativa = True

        self.abrirFun('concatenar')
        # aputandor
        apuntador = self.agregarTemp()
        # apuntador de los strings
        str1 = self.agregarTemp()
        str2 = self.agregarTemp()
        nuevoStr = self.agregarTemp()
        # labels loops
        loop1 = self.agregarLabel()
        salir1 = self.agregarLabel()
        loop2 = self.agregarLabel()
        salir2 = self.agregarLabel()
        # obtener valores
        self.agregarExp(apuntador, 'P', '1', '+')
        self.getStack(str1, apuntador)
        self.agregarExp(apuntador, apuntador, '1', '+')
        self.getStack(str2, apuntador)
        self.agregarExp(nuevoStr, 'H', '', '')
        # recorrer primer string
        self.printLabel(loop1)
        self.getHeap(apuntador, str1)
        self.agregarIf(apuntador, '-1', '==', salir1)
        self.setHeap('H', apuntador)
        self.nextHeap()
        self.agregarExp(str1, str1, '1', '+')
        self.printGoto(loop1)
        self.printLabel(salir1)
        # recorrer segundo string
        self.printLabel(loop2)
        self.getHeap(apuntador, str2)
        self.agregarIf(apuntador, '-1', '==', salir2)
        self.setHeap('H', apuntador)
        self.nextHeap()
        self.agregarExp(str2, str2, '1', '+')
        self.printGoto(loop2)
        self.printLabel(salir2)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', nuevoStr)
        self.cerrarFun()
        self.enNativa = False

    def multiplicarStr(self):
        if self.multStr:
            return
        self.multStr = True
        self.enNativa = True

        self.abrirFun('multStr')
        # aputandor
        apuntador = self.agregarTemp()
        # apuntador de los strings
        string = self.agregarTemp()
        auxiliar = self.agregarTemp()
        veces = self.agregarTemp()
        nuevoStr = self.agregarTemp()
        # labels loops
        loop1 = self.agregarLabel()
        salir1 = self.agregarLabel()
        loop2 = self.agregarLabel()
        salir2 = self.agregarLabel()
        # obtener valores
        self.agregarExp(apuntador, 'P', '1', '+')
        self.getStack(string, apuntador)
        self.agregarExp(auxiliar, string, '', '')
        self.agregarExp(apuntador, apuntador, '1', '+')
        self.getStack(veces, apuntador)
        self.agregarExp(nuevoStr, 'H', '', '')
        # recorrer primer loop de veces
        self.printLabel(loop1)
        self.agregarIf(veces, '0', '==', salir1)
        self.agregarExp(string, auxiliar, '', '')
        # recorrer string
        self.printLabel(loop2)
        self.getHeap(apuntador, string)
        self.agregarIf(apuntador, '-1', '==', salir2)
        self.setHeap('H', apuntador)
        self.nextHeap()
        self.agregarExp(string, string, '1', '+')
        self.printGoto(loop2)
        self.printLabel(salir2)
        self.agregarExp(veces, veces, '1', '-')
        self.printGoto(loop1)
        self.printLabel(salir1)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', nuevoStr)
        self.cerrarFun()
        self.enNativa = False

    def compararStr(self):
        if self.compStr:
            return
        self.compStr = True
        self.enNativa = True

        self.abrirFun('cmpStr')
        # aputandor
        apuntador1 = self.agregarTemp()
        apuntador2 = self.agregarTemp()
        # apuntador de los strings
        str1 = self.agregarTemp()
        str2 = self.agregarTemp()
        # labels loops
        loop = self.agregarLabel()
        salir = self.agregarLabel()
        verdadero = self.agregarLabel()
        falso = self.agregarLabel()
        # obtener valores
        self.agregarExp(apuntador1, 'P', '1', '+')
        self.getStack(str1, apuntador1)
        self.agregarExp(apuntador2, apuntador1, '1', '+')
        self.getStack(str2, apuntador2)
        # recorrer strings
        self.printLabel(loop)
        self.getHeap(apuntador1, str1)
        self.getHeap(apuntador2, str2)
        self.agregarIf(apuntador1, apuntador2, '!=', falso)
        self.agregarIf(apuntador1, '-1', '==', verdadero)
        self.agregarExp(str1, str1, '1', '+')
        self.agregarExp(str2, str2, '1', '+')
        self.printGoto(loop)
        self.printLabel(verdadero)
        self.setStack('P', '1')
        self.printGoto(salir)
        self.printLabel(falso)
        self.setStack('P', '0')
        self.printLabel(salir)
        self.cerrarFun()
        self.enNativa = False

    def upper(self):
        if self.funcUpper:
            return
        self.funcUpper = True
        self.enNativa = True

        self.abrirFun('upper')
        # apuntador
        apuntador = self.agregarTemp()
        # apuntador de los strings
        string = self.agregarTemp()
        nuevo = self.agregarTemp()
        # labels loops
        loop = self.agregarLabel()
        salir = self.agregarLabel()
        falso = self.agregarLabel()
        # obtener valores
        self.agregarExp(apuntador, 'P', '1', '+')
        self.getStack(string, apuntador)
        self.agregarExp(nuevo, 'H', '', '')
        # recorrer string
        self.printLabel(loop)
        self.getHeap(apuntador, string)
        self.agregarIf(apuntador, '-1', '==', salir)
        self.agregarIf(apuntador, '97', '<', falso)
        self.agregarIf(apuntador, '122', '>', falso)
        self.agregarExp(apuntador, apuntador, '32', '-')
        self.printLabel(falso)
        self.setHeap('H', apuntador)
        self.nextHeap()
        self.agregarExp(string, string, '1', '+')
        self.printGoto(loop)
        self.printLabel(salir)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', nuevo)
        self.cerrarFun()
        self.enNativa = False

    def lower(self):
        if self.funcLower:
            return
        self.funcLower = True
        self.enNativa = True

        self.abrirFun('lower')
        # apuntador
        apuntador = self.agregarTemp()
        # apuntador de los strings
        string = self.agregarTemp()
        nuevo = self.agregarTemp()
        # labels loops
        loop = self.agregarLabel()
        salir = self.agregarLabel()
        falso = self.agregarLabel()
        # obtener valores
        self.agregarExp(apuntador, 'P', '1', '+')
        self.getStack(string, apuntador)
        self.agregarExp(nuevo, 'H', '', '')
        # recorrer string
        self.printLabel(loop)
        self.getHeap(apuntador, string)
        self.agregarIf(apuntador, '-1', '==', salir)
        self.agregarIf(apuntador, '65', '<', falso)
        self.agregarIf(apuntador, '90', '>', falso)
        self.agregarExp(apuntador, apuntador, '32', '+')
        self.printLabel(falso)
        self.setHeap('H', apuntador)
        self.nextHeap()
        self.agregarExp(string, string, '1', '+')
        self.printGoto(loop)
        self.printLabel(salir)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setStack('P', nuevo)
        self.cerrarFun()
        self.enNativa = False

    def printMathError(self):
        if self.mathError:
            return
        self.mathError = True
        self.enNativa = True
        self.abrirFun('mathError')
        self.agregarPrint("c", 77)
        self.agregarPrint("c", 65)
        self.agregarPrint("c", 84)
        self.agregarPrint("c", 72)
        self.agregarPrint("c", 32)
        self.agregarPrint("c", 69)
        self.agregarPrint("c", 82)
        self.agregarPrint("c", 82)
        self.agregarPrint("c", 79)
        self.agregarPrint("c", 82)
        self.agregarPrint("c", 10)
        self.cerrarFun()
        self.enNativa = False

    def printOutBounds(self):
        if self.outofBounds:
            return
        self.outofBounds = True
        self.enNativa = True
        self.abrirFun('outOfBounds')
        self.agregarPrint("c", 79)
        self.agregarPrint("c", 85)
        self.agregarPrint("c", 84)
        self.agregarPrint("c", 79)
        self.agregarPrint("c", 70)
        self.agregarPrint("c", 66)
        self.agregarPrint("c", 79)
        self.agregarPrint("c", 85)
        self.agregarPrint("c", 78)
        self.agregarPrint("c", 68)
        self.agregarPrint("c", 83)
        self.agregarPrint("c", 10)
        self.cerrarFun()
        self.enNativa = False
