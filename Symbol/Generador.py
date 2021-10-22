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

    def limpiarTodo(self):
        # Contadores
        self.totTemp = 0
        self.codigo = ''
        # Lista de Temporales
        self.temps = []
        Generador.generator = Generador()

    # CODE
    def getCodigo(self):
        return f'{self.codigo}'

    def agregarCodigo(self, codigo):
        self.codigo = self.codigo + codigo

    def agregarCometario(self, comment):
        self.agregarCodigo(f'/* {comment} */')

    def getInstancia(self):
        if Generador.generador is None:
            Generador.generador = Generador()
        return Generador.generador

    # Manejo de Temporales
    def agregarTemp(self):
        temp = f't{self.totTemp}'
        self.totTemp += 1
        self.temps.append(temp)
        return temp

    # EXPRESIONES
    def agregarExp(self, result, left, right, op):
        self.agregarCodigo(f'{result}={left}{op}{right};\n')

    # INSTRUCCIONES
    def agregarPrint(self, type, value):
        self.agregarCodigo(f'fmt.Printf("%{type}", {value});\n')

    def printTrue(self):
        self.agregarPrint("s", "t")
        self.agregarPrint("s", "r")
        self.agregarPrint("s", "u")
        self.agregarPrint("s", "e")
