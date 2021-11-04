from datetime import datetime

from Symbol.Simbolo import *


class Entorno:

    def __init__(self, prev, nombre):
        self.prev = prev
        self.nombre = nombre
        self.tamano = 0
        self.breakl = ''
        self.continuel = ''
        self.returnl = ''
        if prev is not None:
            self.tamano = self.prev.tamano
            self.breakl = self.prev.breakl
            self.continuel = self.prev.continuel
            self.returnl = self.prev.returnl
        self.variables = {}
        self.funciones = {}
        self.structs = {}
        self.simbols = []
        self.errors = []

    def guardarVarGlobal(self, idVar, tipo, enHeap, linea, columna):
        glb = self.getGlobal()
        if idVar in glb.variables.keys():
            print("variable ya existe")
        else:
            nuevoSimbolo = Simbolo(idVar, tipo, self.tamano, True, enHeap)
            self.guardarTS(idVar, linea, columna, tipo)
            glb.tamano += 1
            glb.variables[idVar] = nuevoSimbolo
        var = glb.variables[idVar]
        return var

    def guardarVarLocal(self, idVar, tipo, enHeap, linea, columna):
        if idVar in self.variables.keys():
            print("Variable ya existe")
        else:
            nuevoSimbolo = Simbolo(idVar, tipo, self.tamano, self.prev is None, enHeap)
            self.guardarTS(idVar, linea, columna, tipo)
            self.tamano += 1
            self.variables[idVar] = nuevoSimbolo
        return self.variables[idVar]

    def guardarVar(self, idVar, tipo, enHeap, linea, columna):
        entorno = self
        while True:
            if idVar in entorno.variables.keys():
                print("Variable ya existe")
                return entorno.variables[idVar]
            if entorno.nombre != "WHILE" and entorno.nombre != "FOR":
                break
            else:
                entorno = entorno.prev

        nuevoSimbolo = Simbolo(idVar, tipo, self.tamano, self.prev is None, enHeap)
        self.guardarTS(idVar, linea, columna, tipo)
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

    def moverGlobal(self, idVar):
        glb = self.getGlobal()
        var = glb.getVar(idVar)
        if var is not None:
            self.variables[idVar] = var
        else:
            print("variable global no existe: " + idVar)

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
        simbol = TablaS(id, clas, self.nombre, linea, columna)
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