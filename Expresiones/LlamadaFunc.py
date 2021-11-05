from Abstract.Expresion import *
from Abstract.Return import *
from Symbol.Entorno import *
from Symbol.Generador import *


class LlamadaFunc(Expresion):

    def __init__(self, id, params, linea, columna):
        Expresion.__init__(self, linea, columna)
        self.id = id
        self.params = params

    def compilar(self, entorno):
        func = entorno.getFunc(self.id)
        if func != None:
            valoresParams = []

            genAux = Generador()
            generador = genAux.getInstancia()
            glb = entorno.getGlobal()
            tamano = entorno.tamano
            glbtam = glb.tamano
            glb.tamano = 0
            for param in self.params:
                valoresParams.append(param.compilar(entorno))
            temp = generador.agregarTemp()

            generador.agregarExp(temp, 'P', tamano + 1, '+')
            aux = 0
            for param in valoresParams:
                aux = aux + 1
                generador.setStack(temp, param.valor)
                if aux != len(valoresParams):
                    generador.agregarExp(temp, temp, '1', '+')

            generador.nuevoEnt(tamano)
            generador.llamarFun(self.id)
            generador.getStack(temp, 'P')
            generador.regresarEnt(tamano)

            # Verificar tipo de la funcion. Boolean es distinto
            glb.tamano = glbtam
            if func.tipo is None:
                return
            if func.tipo == Tipo.BOOLEAN:
                if self.truel == '' and self.falsel == '':
                    self.truel = generador.agregarLabel()
                    self.falsel = generador.agregarLabel()
                generador.agregarIf(temp, '1', '==', self.truel)
                generador.printGoto(self.falsel)
                ret = Return(temp, func.tipo, False)
                ret.truel = self.truel
                ret.falsel = self.falsel
                return ret
            else:
                return Return(temp, func.tipo, True)
