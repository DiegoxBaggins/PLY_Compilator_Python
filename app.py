import sys
import json
from flask import Flask, render_template, url_for, redirect, request
from Symbol.Generador import *
from Analyzer.Grammar import parse


app = Flask(__name__)


@app.route('/')
def slash():  # put application's code here
    return redirect(url_for('home'))


@app.route('/home')
def home():  # put application's code here
    return render_template('index.html')


@app.route('/analisis',  methods=["POST", "GET"])
def analisis():  # put application's code here
    if request.method == "POST":
        tipoEntrada = request.form['procesar']
        dic = request.form
        codigo = dic["txt1"]
        resultado = "Resultado"
        if tipoEntrada == "Compilar":
            resultado = compilar(codigo)
        elif tipoEntrada == "Mirilla":
            resultado = "Optimizacion de Mirilla"
        elif tipoEntrada == "Bloques":
            resultado = "Optimizacion por bloques"
        return render_template('analisis.html', text1=codigo, text2=resultado)
    else:
        return render_template('analisis.html', text1="escribe aqui tu codigo", text2="Output Console")


@app.route('/reports',  methods=["POST", "GET"])
def reports():  # put application's code here
    errores = []
    simbolos = []
    bandVar = False
    bandErr = False
    bandOpt = False
    if request.method == "POST":
        tipoEntrada = request.form['procesar']
        if tipoEntrada == "Simbolos":
            with open('simbols.json') as json_file:
                simbolos = json.load(json_file)
            bandVar = True
        elif tipoEntrada == "Errores":
            with open('errors.json') as json_file:
                errores = json.load(json_file)
            bandErr = True
        elif tipoEntrada == "Optimizacion":
            bandOpt = True
        return render_template('reports.html', errores=errores, simbols=simbolos, bandVar=bandVar, bandErr=bandErr,
                               bandOpt=bandOpt)
    else:
        return render_template('reports.html', errores=errores, simbols=simbolos, bandVar=bandVar, bandErr=bandErr,
                               bandOpt=bandOpt)


if __name__ == '__main__':
    app.run()


def compilar(entrada):
    codigo = ""
    genAux = Generador()
    genAux.limpiarTodo()
    generador = genAux.getInstancia()

    newEnv = Entorno(None, "GLOBAL")
    ast = parse(entrada)
    for instr in ast:
        instr.compilar(newEnv)
    codigo += generador.getCodigo()
    errores = newEnv.errors
    with open('errors.json', 'w') as outfile:
        json.dump(errores, outfile)
    variables = newEnv.simbols
    with open('simbols.json', 'w') as outfile:
        json.dump(variables, outfile)
    return codigo
