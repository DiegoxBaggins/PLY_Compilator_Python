from .Entorno import Entorno


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
        Generador.generator = None

    # CODIGO
    def getCodigo(self):
        return f'{self.codigo}'

    def agregarCodigo(self, codigo):
        self.codigo = self.codigo + codigo

    def agregarCometario(self, comentario):
        self.agregarCodigo(f'/* {comentario} */\n')

    def getInstancia(self):
        if Generador.generador is None:
            Generador.generador = Generador()
        return Generador.generador

    def getCabeza(self):
        codigo = "package main \nimport (\n\t\"fmt\"\n)\n\nvar "
        temporales = ""
        print(self.temps)
        for temp in self.temps:
            temporales += temp + ", "
        codigo += temporales[:len(temporales) - 2]
        codigo += " float64;\n\n"
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
        self.agregarCodigo(f'fmt.Printf("%{tipo}", int({valor}));\n')

    # IF
    def agregarIf(self, left, right, op, label):
        self.agregarCodigo(f'if {left} {op} {right} {{goto {label};}}\n')

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
