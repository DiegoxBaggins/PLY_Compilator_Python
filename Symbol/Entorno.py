from datetime import datetime

from Symbol.Simbolo import *


class Entorno:

    def __init__(self, prev):
        self.prev = prev
        self.tamano = 0
        self.lblBreak = ''
        self.lblContinue = ''
        self.lblReturn = ''
        if prev is not None:
            self.tamano = self.prev.tamano
            self.lblBreak = self.prev.lblBreak
            self.lblContinue = self.prev.lblContinue
            self.lblReturn = self.prev.lblReturn
        self.variables = {}
        self.funciones = {}
        self.structs = {}
        self.simbols = []
        self.errors = []

    def guardarVar(self, idVar, tipo, enHeap):
        if idVar in self.variables.keys():
            print("Variable ya existe")
        else:
            nuevoSimbolo = Simbolo(idVar, tipo, self.tamano, self.prev is None, enHeap)
            self.tamano += 1
            self.variables[idVar] = nuevoSimbolo
        return self.variables[idVar]

    def newVarStruct(self, idVar, obj):
        env = self
        while env.prev is not None:
            if idVar in env.variables.keys():
                env.variables[idVar] = obj
                return
            env = env.prev
        self.variables[idVar] = obj

    def newFunc(self, idFunc, function):
        if idFunc in self.funciones.keys():
            print("Función repetida")
        else:
            self.funciones[idFunc] = function

    def newStruct(self, idStruct, struct):
        if idStruct in self.structs.keys():
            print("Struct repetido")
        else:
            self.structs[idStruct] = struct

    def getVar(self, idVar):
        env = self
        while env is not None:
            if idVar in env.variables.keys():
                return env.variables[idVar]
            env = env.prev
        return None

    def getFunc(self, idFunc):
        env = self
        while env is not None:
            if idFunc in env.funciones.keys():
                return env.funciones[idFunc]
            env = env.prev
        return None

    def getStruct(self, idStruct):
        env = self
        while env is not None:
            if idStruct in env.structs.keys():
                return env.structs[idStruct]
            env = env.prev
        return None

    def getGlobal(self):
        env = self
        while env.prev is not None:
            env = env.prev
        return env

    def guardarTS(self, id, linea, columna, clas):
        env = self.getGlobal()
        simbol = TablaS(id, clas, 'entorno', linea, columna)
        env.simbols.append(simbol)

    def guardarError(self, descripcion, linea, columna):
        now = datetime.now()
        env = self.getGlobal()
        num = len(env.errors) + 1
        fecha = now.strftime("%d/%m/%Y %H:%M:%S")
        error = Error(num, descripcion, linea, columna, fecha)
        env.errors.append(error)


def TablaS(id, tipo, ambito, linea, columna):
    if isinstance(tipo, Enum):
        tp = tipo.name
    else:
        tp = tipo
    return [id, tp, ambito, linea, columna]


def Error(num, descripcion, linea, columna, fecha):
    return [num, descripcion, linea, columna, fecha]