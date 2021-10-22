from Instruction.Print import *
from Instruction.Sentencia import *
from Instruction.If import *
from Instruction.Declaracion import *
from Instruction.Funcion import *
from Instruction.Parametro import *
from Instruction.ReturnIns import *
from Instruction.While import *
from Instruction.For import *
from Instruction.ControlNS import *
from Structs.Nuevo import *
from Structs.Asignacion import *
from Structs.Acceso import *
from Arreglos.Nuevo import *
from Arreglos.Acceso import *
from Arreglos.Asignacion import *
from Arreglos.Cut import *
from Arreglos.Funcs import *

from Expresiones.Literal import *
from Expresiones.Aritmetico import *
from Expresiones.Relacional import *
from Expresiones.Nativas import *
from Expresiones.Acceso import *
from Expresiones.LlamadaFunc import *

rw = {
    "NOTHING": "NOTHING", "INT64": "INT64", "FLOAT64": "FLOAT64", "BOOL": "BOOL", "CHAR": "CHAR", "STRING": "STRING",
    "TRUE": "TRUE", "FALSE": "FALSE", "LOCAL": "LOCAL", "GLOBAL": "GLOBAL",
    "IF": "IF", "ELSE": "ELSE", "ELSEIF": "ELSEIF", "PRINT": "PRINT", "PRINTLN": "PRINTLN", "END": "END",
    "FUNCTION": "FUNCTION", "RETURN": "RETURN", "WHILE": "WHILE", "FOR": "FOR", "IN": "IN", "BREAK": "BREAK",
    "CONTINUE": "CONTINUE", "STRUCT": "STRUCT", "MUTABLE": "MUTABLE", "PUSH": "PUSH", "POP": "POP", "LENGTH": "LENGTH",
    "LOG10": "LOG10", "LOG": "LOG", "SIN": "SIN", "COS": "COS", "TAN": "TAN", "SQRT": "SQRT", "UPPERCASE": "UPPERCASE",
    "LOWERCASE": "LOWERCASE", "PARSE": "PARSE", "TRUNC": "TRUNC", "FLOAT": "FLOAT", "TYPEOF": "TYPEOF",
}

tokens = [
             "ID", "INTID", "FLOATID", "STRINGID", "CHARID",
             "IGUAL", "PUNTO", "COMA", "DOSPUNTOS", "PUNTOCOMA",
             "PARIZQ", "PARDER", "CORIZQ", "CORDER",
             "MAS", "MENOS", "MULT", "DIV", "POT", "MOD",
             "AND", "OR", "NOT",
             "MAYOR", "MENOR", "MAYORIGUAL", "MENORIGUAL", "IGUALES", "DISTINTOS",
         ] + list(rw.values())

t_IGUAL = r'='
t_PUNTO = r'\.'
t_DOSPUNTOS = r':'
t_PUNTOCOMA = r';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_MAS = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_POT = r'\^'
t_MOD = r'%'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_IGUALES = r'=='
t_DISTINTOS = r'!='


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = rw.get(t.value.upper(), 'ID')
    return t


def t_FLOATID(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("ERROR IN PARSE TO FLOAT")
        t.value = 0
    return t


def t_INTID(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("ERROR IN PARSE TO INT")
        t.value = 0
    return t


def t_STRINGID(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_CHARID(t):
    r'\'.*?\''
    t.value = t.value[1:-1]
    return t


t_ignore = " \t"


def t_COMENTARIO(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count("\n")


def t_COMLINEA(t):
    r'\#.*\n'
    t.lexer.lineno += 1


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex

lexer = lex.lex()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALES', 'DISTINTOS'),
    ('left', 'MAYORIGUAL', 'MENORIGUAL', 'MAYOR', 'MENOR'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'POT'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
    ('left', 'PARIZQ', 'PARDER', 'CORIZQ', 'CORDER')
)


# SYNTACTIC ANALYSIS

def p_start(t):
    'inicio : instruccionesglb'
    t[0] = t[1]
    return t[0]


# instrucciones Globales
def p_instruccionesglb(t):
    '''instruccionesglb : instruccionesglb instruccionglb
                        | instruccionglb'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]


def p_instruccionglb(t):
    '''instruccionglb  : funcionINS PUNTOCOMA
                       | declaracionglb PUNTOCOMA
                       | printINS PUNTOCOMA
                       | llamadaFunc PUNTOCOMA
                       | ifINS PUNTOCOMA
                       | whileINS PUNTOCOMA
                       | forINS PUNTOCOMA
                       | newStruct PUNTOCOMA
                       | pushArreglo PUNTOCOMA
                       | asignacionStruct PUNTOCOMA
                       | asignacionArreglo PUNTOCOMA'''
    t[0] = t[1]


# ------------------------------------------------Declaracion Global
def p_declaracionglb(t):
    '''declaracionglb : ID
                      | ID IGUAL expresion
                      | ID IGUAL expresion DOSPUNTOS DOSPUNTOS tipos'''
    if len(t) == 2:
        t[0] = Declaracion(TipoAcceso.GLOBAL, t[1], None, Tipo.UNDEFINED, t.lineno(1), t.lexpos(0))
    elif len(t) == 4:
        t[0] = Declaracion(TipoAcceso.GLOBAL, t[1], t[3], Tipo.UNDEFINED, t.lineno(1), t.lexpos(0))
    elif len(t) == 7:
        t[0] = Declaracion(TipoAcceso.GLOBAL, t[1], t[3], t[6], t.lineno(1), t.lexpos(0))


# -------------------------------------------------Declaracion func
def p_funcionINS(t):
    '''funcionINS : FUNCTION ID PARIZQ PARDER sentencia END
                  | FUNCTION ID PARIZQ params PARDER sentencia END'''
    if len(t) == 7:
        t[0] = Function(t[2], [], t[5], t.lineno(1), t.lexpos(0))
    else:
        t[0] = Function(t[2], t[4], t[6], t.lineno(1), t.lexpos(0))


def p_decParams(t):
    '''params : params COMA ID
              | params COMA ID DOSPUNTOS DOSPUNTOS tipos
              | ID
              | ID DOSPUNTOS DOSPUNTOS tipos'''
    if len(t) == 2 or len(t) == 5:
        t[0] = [Parametro(t[1], t.lineno(1), t.lexpos(1))]
    else:
        t[1].append(Parametro(t[3], t.lineno(3), t.lexpos(3)))
        t[0] = t[1]


# -------------------------------------------------Llamada func
def p_llamadaFunc(t):
    '''llamadaFunc : ID PARIZQ PARDER
                   | ID PARIZQ listParams PARDER'''
    if len(t) == 4:
        t[0] = LlamadaFunc(t[1], [], t.lineno(1), t.lexpos(1))
    else:
        t[0] = LlamadaFunc(t[1], t[3], t.lineno(1), t.lexpos(1))


def p_llamadaPar(t):
    '''listParams :  listParams COMA expresion
                  | expresion'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]


# -------------------------------------------------Return
def p_return(t):
    '''returnINS : RETURN
                 | RETURN expresion'''
    if len(t) == 2:
        t[0] = ReturnIns(None, t.lineno(1), t.lexpos(1))
    else:
        t[0] = ReturnIns(t[2], t.lineno(1), t.lexpos(1))


# -------------------------------------------------Instrucciones locales
def p_instrucciones(t):
    '''instrucciones : instrucciones instruccion
                    | instruccion'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]


def p_instruccion(t):
    '''instruccion  : declaracionINS PUNTOCOMA
                    | printINS PUNTOCOMA
                    | llamadaFunc PUNTOCOMA
                    | ifINS PUNTOCOMA
                    | returnINS PUNTOCOMA
                    | whileINS PUNTOCOMA
                    | forINS PUNTOCOMA
                    | breakINS PUNTOCOMA
                    | continueINS PUNTOCOMA
                    | newStruct PUNTOCOMA
                    | pushArreglo PUNTOCOMA
                    | asignacionStruct PUNTOCOMA
                    | asignacionArreglo PUNTOCOMA'''
    t[0] = t[1]


# ---------------------------------------------------Sentencia
def p_sentencia(t):
    '''sentencia : instrucciones'''
    t[0] = Sentencia(t[1], t.lineno(1), t.lexpos(0))


# ----------------------------------------------------PRINT
def p_printlnINS(t):
    '''printINS  : PRINTLN PARIZQ listParams PARDER
                 | PRINTLN PARIZQ PARDER'''
    if len(t) == 5:
        t[0] = Print(t[3], t.lineno(1), t.lexpos(0), True)
    else:
        t[0] = Print([Literal("", Tipo.STRING, t.lineno(1), t.lexpos(0))], t.lineno(1), t.lexpos(0), True)


def p_printINS(t):
    '''printINS  : PRINT PARIZQ listParams PARDER
                 | PRINT PARIZQ PARDER'''
    if len(t) == 5:
        t[0] = Print(t[3], t.lineno(1), t.lexpos(0))
    else:
        t[0] = Print([Literal("", Tipo.STRING, t.lineno(1), t.lexpos(0))], t.lineno(1), t.lexpos(0))


# ---------------------------------------------------Declaracion Local
def p_declaracionINS(t):
    '''declaracionINS : ID
                      | ID IGUAL expresion
                      | ID IGUAL expresion DOSPUNTOS DOSPUNTOS tipos
                      | accesos ID
                      | accesos ID IGUAL expresion
                      | accesos ID IGUAL expresion DOSPUNTOS DOSPUNTOS tipos'''
    if len(t) == 2:
        t[0] = Declaracion(TipoAcceso.VACIO, t[1], None, Tipo.UNDEFINED, t.lineno(1), t.lexpos(0))
    elif len(t) == 4:
        t[0] = Declaracion(TipoAcceso.VACIO, t[1], t[3], Tipo.UNDEFINED, t.lineno(1), t.lexpos(0))
    elif len(t) == 7:
        t[0] = Declaracion(TipoAcceso.VACIO, t[1], t[3], t[6], t.lineno(1), t.lexpos(0))
    elif len(t) == 3:
        t[0] = Declaracion(t[1], t[2], None, Tipo.UNDEFINED, t.lineno(1), t.lexpos(0))
    elif len(t) == 5:
        t[0] = Declaracion(t[1], t[2], t[4], Tipo.UNDEFINED, t.lineno(1), t.lexpos(0))
    elif len(t) == 8:
        t[0] = Declaracion(t[0], t[2], t[4], t[7], t.lineno(1), t.lexpos(0))


def p_tipos(t):
    '''tipos : INT64
             | FLOAT64
             | STRING
             | BOOL
             | CHAR'''
    valor = str(t[1])
    if "Int64" in valor:
        t[0] = Tipo.INT
    if "Float64" in valor:
        t[0] = Tipo.FLOAT
    if "String" in valor:
        t[0] = Tipo.STRING
    if "Bool" in valor:
        t[0] = Tipo.BOOLEAN
    if "Char" in valor:
        t[0] = Tipo.CHAR


def p_accesos(t):
    '''accesos : LOCAL
               | GLOBAL'''
    valor = str(t[1])
    if "local" in valor:
        t[0] = TipoAcceso.LOCAL
    if "global" in valor:
        t[0] = TipoAcceso.GLOBAL


# ---------------------------------------------------ASIGNACION STRUCT
def p_asignacionStruct(t):
    'asignacionStruct : accesoStruct IGUAL expresion'
    t[0] = AsignacionStruct(t[1], t[3], t.lineno(1), t.lexpos(1))


# ---------------------------------------------------ASIGNACION ARREGLO
def p_asignacionArreglo(t):
    'asignacionArreglo : accesoArreglo IGUAL expresion'
    t[0] = AsignacionArreglo(t[1], t[3], t.lineno(1), t.lexpos(1))


# ---------------------------------------------------While
def p_whileINS(t):
    'whileINS : WHILE expresion sentencia END'
    t[0] = While(t[2], t[3], t.lineno(1), t.lexpos(0))


# ---------------------------------------------------For
def p_forINS(t):
    '''forINS : FOR ID IN expresion DOSPUNTOS expresion sentencia END
              | FOR ID IN expresion sentencia END'''
    if len(t) == 7:
        t[0] = For(t[2], t[4], None, t[5], t.lineno(1), t.lexpos(0))
    else:
        t[0] = For(t[2], t[4], t[6], t[7], t.lineno(1), t.lexpos(0))


# ---------------------------------------------------Break
def p_breakINS(t):
    'breakINS : BREAK'
    t[0] = ControlIns(Tipo.BREAKINS, t.lineno(1), t.lexpos(0))


# ---------------------------------------------------Continue
def p_continueINS(t):
    'continueINS : CONTINUE'
    t[0] = ControlIns(Tipo.CONTINUEINS, t.lineno(1), t.lexpos(0))


# ---------------------------------------------------IF
def p_ifINS(t):
    '''ifINS : IF expresion sentencia END
             | IF expresion sentencia ELSE sentencia END
             | IF expresion sentencia elseIfLista END'''
    if len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0))
    elif len(t) == 7:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[5])
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[4])


def p_elseIfLista(t):
    '''elseIfLista   : ELSEIF expresion sentencia
                     | ELSEIF expresion sentencia ELSE sentencia
                     | ELSEIF expresion sentencia elseIfLista'''
    if len(t) == 4:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0))
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[5])
    elif len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[4])


# --------------------------------------------------Declarar Struct
def p_newStruct(t):
    '''newStruct : STRUCT ID atributosStr END
                 | MUTABLE STRUCT ID atributosStr END'''
    if len(t) == 5:
        t[0] = NuevoStruct(TipoStruct.NOMUTABLE, t[2], t[3], t.lineno(1), t.lexpos(0))
    else:
        t[0] = NuevoStruct(TipoStruct.MUTABLE, t[3], t[4], t.lineno(1), t.lexpos(0))


def p_atributosStr(t):
    '''atributosStr : atributosStr ID PUNTOCOMA
                    | ID PUNTOCOMA
                    | atributosStr ID DOSPUNTOS DOSPUNTOS tipos PUNTOCOMA
                    | ID DOSPUNTOS DOSPUNTOS tipos PUNTOCOMA'''
    if len(t) == 3:
        t[0] = [Return(t[1], Tipo.UNDEFINED, "")]
    elif len(t) == 6:
        t[0] = [Return(t[1], t[4], "")]
    elif len(t) == 4:
        t[1].append(Return(t[2], Tipo.UNDEFINED, ""))
        t[0] = t[1]
    else:
        t[1].append(Return(t[2], t[5], ""))
        t[0] = t[1]


# --------------------------------------------------EXPRESIONES
def p_expresion(t):
    '''expresion    : MENOS expresion %prec UMINUS
                    | NOT expresion %prec UMINUS

                    | expresion MAS expresion
                    | expresion MENOS expresion
                    | expresion MULT expresion
                    | expresion DIV expresion
                    | expresion MOD expresion
                    | expresion POT expresion

                    | expresion MAYOR expresion
                    | expresion MENOR expresion
                    | expresion MAYORIGUAL expresion
                    | expresion MENORIGUAL expresion
                    | expresion IGUALES expresion
                    | expresion DISTINTOS expresion

                    | expresion OR expresion
                    | expresion AND expresion
                    | expValor'''
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 3:
        # UMINUS
        if t[1] == "-":
            t[0] = Aritmetico(t[2], t[2], OperacionAritmetica.MENOS, t.lineno(1), t.lexpos(0))
        elif t[1] == "!":
            t[0] = Relacional(t[2], t[2], OperacionRelacional.NOT, t.lineno(1), t.lexpos(0))
    else:
        if t[2] == "+":
            t[0] = Aritmetico(t[1], t[3], OperacionAritmetica.SUMA, t.lineno(2), t.lexpos(0))
        elif t[2] == "-":
            t[0] = Aritmetico(t[1], t[3], OperacionAritmetica.RESTA, t.lineno(2), t.lexpos(0))
        elif t[2] == "*":
            t[0] = Aritmetico(t[1], t[3], OperacionAritmetica.MULTI, t.lineno(2), t.lexpos(0))
        elif t[2] == "/":
            t[0] = Aritmetico(t[1], t[3], OperacionAritmetica.DIV, t.lineno(2), t.lexpos(0))
        elif t[2] == "%":
            t[0] = Aritmetico(t[1], t[3], OperacionAritmetica.MODULO, t.lineno(2), t.lexpos(0))
        elif t[2] == "^":
            t[0] = Aritmetico(t[1], t[3], OperacionAritmetica.POTENCIA, t.lineno(2), t.lexpos(0))
        elif t[2] == ">":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.MAYOR, t.lineno(2), t.lexpos(2))
        elif t[2] == "<":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.MENOR, t.lineno(2), t.lexpos(2))
        elif t[2] == ">=":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.MAYORIGUAL, t.lineno(2), t.lexpos(2))
        elif t[2] == "<=":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.MENORIGUAL, t.lineno(2), t.lexpos(2))
        elif t[2] == "==":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.IGUALES, t.lineno(2), t.lexpos(2))
        elif t[2] == "!=":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.DISTINTOS, t.lineno(2), t.lexpos(2))
        elif t[2] == "||":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.OR, t.lineno(2), t.lexpos(2))
        elif t[2] == "&&":
            t[0] = Relacional(t[1], t[3], OperacionRelacional.AND, t.lineno(2), t.lexpos(2))


def p_expValor(t):
    '''expValor : PARIZQ expresion PARDER
                | INTID
                | FLOATID
                | STRINGID
                | expCHAR
                | expNativas
                | TRUE
                | FALSE
                | ID
                | NOTHING
                | llamadaFunc
                | accesoStruct
                | defArreglo
                | accesoArreglo
                | cutArreglo
                | popArreglo
                | lenArreglo'''
    if len(t) == 2:
        if t.slice[1].type == "INTID":
            t[0] = Literal(int(t[1]), Tipo.INT, t.lineno(1), t.lexpos(0))
        elif t.slice[1].type == "FLOATID":
            t[0] = Literal(float(t[1]), Tipo.FLOAT, t.lineno(1), t.lexpos(0))
        elif t.slice[1].type == "ID":
            t[0] = Acceso(t[1], t.lineno(1), t.lexpos(1))
        elif isinstance(t[1], str):
            valor = str(t[1])
            if "true" in valor:
                t[0] = Literal(True, Tipo.BOOLEAN, t.lineno(1), t.lexpos(0))
            elif "false" in valor:
                t[0] = Literal(False, Tipo.BOOLEAN, t.lineno(1), t.lexpos(0))
            elif "nothing" in valor:
                t[0] = Literal(None, Tipo.UNDEFINED, t.lineno(1), t.lexpos(0))
            else:
                t[0] = Literal(str(t[1]), Tipo.STRING, t.lineno(1), t.lexpos(0))
        else:
            t[0] = t[1]
    else:
        t[0] = t[2]


def p_CHARS(t):
    '''expCHAR : CHARID'''
    t[0] = Literal(str(t[1]), Tipo.CHAR, t.lineno(1), t.lexpos(0))


# -------------------------------------------------FUNCIONES NATIVAS
def p_defNativas(t):
    '''expNativas : LOG10 PARIZQ expresion PARDER
                  | LOG PARIZQ expresion COMA expresion PARDER
                  | SIN PARIZQ expresion PARDER
                  | COS PARIZQ expresion PARDER
                  | TAN PARIZQ expresion PARDER
                  | SQRT PARIZQ expresion PARDER
                  | UPPERCASE PARIZQ expresion PARDER
                  | LOWERCASE PARIZQ expresion PARDER
                  | PARSE PARIZQ INT64 COMA expresion PARDER
                  | PARSE PARIZQ FLOAT64 COMA expresion PARDER
                  | TRUNC PARIZQ expresion PARDER
                  | FLOAT PARIZQ expresion PARDER
                  | STRING PARIZQ expresion PARDER
                  | TYPEOF PARIZQ expresion PARDER'''
    valor = str(t[1])
    if "log10" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.LOG10, t.lineno(1), t.lexpos(0))
    elif "log" in valor:
        t[0] = Nativo(t[3], t[5], FuncionNativa.LOGBAS, t.lineno(1), t.lexpos(0))
    elif "sin" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.SEN, t.lineno(1), t.lexpos(0))
    elif "cos" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.COS, t.lineno(1), t.lexpos(0))
    elif "tan" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.TAN, t.lineno(1), t.lexpos(0))
    elif "sqrt" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.RAIZ, t.lineno(1), t.lexpos(0))
    elif "uppercase" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.UPPER, t.lineno(1), t.lexpos(0))
    elif "lowercase" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.LOWER, t.lineno(1), t.lexpos(0))
    elif "parse" in valor:
        valor2 = str(t[3])
        if "Int64" in valor2:
            t[0] = Nativo(t[5], Tipo.INT, FuncionNativa.PARSE, t.lineno(1), t.lexpos(0))
        else:
            t[0] = Nativo(t[5], Tipo.FLOAT, FuncionNativa.PARSE, t.lineno(1), t.lexpos(0))
    elif "trunc" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.TRUNC, t.lineno(1), t.lexpos(0))
    elif "float" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.FLOAT, t.lineno(1), t.lexpos(0))
    elif "string" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.STRING, t.lineno(1), t.lexpos(0))
    elif "typeof" in valor:
        t[0] = Nativo(t[3], t[3], FuncionNativa.TYPEOF, t.lineno(1), t.lexpos(0))


# -------------------------------------------------ACCESO STRUCT
def p_accesoStructST(t):
    '''accesoStruct : ID PUNTO ID
                    | accesoStruct PUNTO ID'''
    if len(t) == 4:
        t[0] = AccesoStruct(t[1], t[3], t.lineno(1), t.lexpos(1))
    else:
        t[0] = AccesoStruct(t[1], t[3], t.lineno(1), t.lexpos(1))


# -------------------------------------------------METODOS ARREGLOS
def p_defArreglo(t):
    'defArreglo : CORIZQ listParams CORDER'
    t[0] = NuevoArray(t[2], t.lineno(1), t.lexpos(1))


def p_accesoArreglo(t):
    '''accesoArreglo : ID CORIZQ expresion CORDER
                    | accesoArreglo CORIZQ expresion CORDER'''
    if len(t) == 5:
        t[0] = AccesoArreglo(t[1], t[3], t.lineno(1), t.lexpos(1))
    else:
        t[0] = AccesoArreglo(t[1], t[3], t.lineno(1), t.lexpos(1))


def p_cutArreglo(t):
    '''cutArreglo : accesoArreglo CORIZQ expresion DOSPUNTOS expresion CORDER
                  | ID CORIZQ expresion DOSPUNTOS expresion CORDER'''
    t[0] = CutArreglo(t[1], t[3], t[5], t.lineno(1), t.lexpos(1))


def p_popArreglo(t):
    '''popArreglo : POP NOT PARIZQ accesoArreglo PARDER
                  | POP NOT PARIZQ ID PARDER'''
    t[0] = FuncArreglo(t[4], None, FuncionArreglo.POP, t.lineno(1), t.lexpos(1))


def p_lenArreglo(t):
    '''lenArreglo : LENGTH PARIZQ accesoArreglo PARDER
                  | LENGTH PARIZQ ID PARDER'''
    t[0] = FuncArreglo(t[3], None, FuncionArreglo.LENGTH, t.lineno(1), t.lexpos(1))


def p_pushArreglo(t):
    '''pushArreglo : PUSH NOT PARIZQ accesoArreglo COMA expresion PARDER
                   | PUSH NOT PARIZQ ID COMA expresion PARDER'''
    t[0] = FuncArreglo(t[4], t[6], FuncionArreglo.PUSH, t.lineno(1), t.lexpos(1))


def p_error(t):
    print(t)
    print("Syntactic error in '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()


def parse(strs):
    return parser.parse(strs)
