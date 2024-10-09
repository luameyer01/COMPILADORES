from flask import Flask, request, jsonify, render_template
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# ------------- Analizador léxico -------------
tokens = [
    'PROGRAMA', 'ID', 'PUNTOCOMA', 'PARENTESIS_ABIERTO', 'PARENTESIS_CERRADO', 
    'LLAVE_ABIERTA', 'LLAVE_CERRADA', 'CORCHETE_ABIERTO', 'CORCHETE_CERRADO',
    'PUNTO', 'COMA', 'IGUAL', 'MAS', 'STRING'
]

# Palabras reservadas de C#
reserved = {
    'using': 'USING',
    'System': 'SYSTEM',
    'namespace': 'NAMESPACE',
    'class': 'CLASS',
    'static': 'STATIC',
    'void': 'VOID',
    'Main': 'MAIN',
    'string': 'STRING',
    'args': 'ARGS',
    'Console': 'CONSOLE',
    'WriteLine': 'WRITELINE',
}

tokens = tokens + list(reserved.values())

# Reglas de expresión regular para tokens simples
t_PUNTOCOMA = r'\;'
t_COMA = r'\,'
t_PUNTO = r'\.'
t_IGUAL = r'='
t_PARENTESIS_ABIERTO = r'\('
t_PARENTESIS_CERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'
t_CORCHETE_ABIERTO = r'\['
t_CORCHETE_CERRADO = r'\]'
t_MAS = r'\+'
t_ignore = ' \t'

# Reglas para identificar identificadores y cadenas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es palabra clave
    return t

def t_STRING(t):
    r'\".*?\"'
    return t

# Manejar los saltos de línea
def t_newline(t):
    r'(\r\n|\n|\r)+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
errores_lexicos = []

def t_error(t):
    error_msg = f"Carácter no reconocido: '{t.value[0]}' en la línea {t.lexer.lineno}"
    errores_lexicos.append(error_msg)
    t.lexer.skip(1)

# ------------- Analizador sintáctico -------------
errores_sintacticos = []

# Definir reglas gramaticales para C#
def p_program(p):
    '''programa : USING SYSTEM PUNTOCOMA NAMESPACE ID LLAVE_ABIERTA class_decl LLAVE_CERRADA'''
    pass

def p_class_decl(p):
    '''class_decl : CLASS ID LLAVE_ABIERTA static_main LLAVE_CERRADA'''
    pass

def p_static_main(p):
    '''static_main : STATIC VOID MAIN PARENTESIS_ABIERTO STRING CORCHETE_ABIERTO CORCHETE_CERRADO ARGS PARENTESIS_CERRADO LLAVE_ABIERTA statements LLAVE_CERRADA'''
    pass

def p_statements(p):
    '''statements : statement statements
                | statement'''
    pass

def p_statement_writeline(p):
    '''statement : SYSTEM PUNTO CONSOLE PUNTO WRITELINE PARENTESIS_ABIERTO STRING PARENTESIS_CERRADO PUNTOCOMA'''
    pass

# Manejo de errores sintácticos
MAX_ERRORES_SINTACTICOS = 11

def p_error(p):
    if len(errores_sintacticos) >= MAX_ERRORES_SINTACTICOS:
        return

    if p:
        error_msg = f"Error sintáctico en '{p.value}' en la línea {p.lineno}"
        errores_sintacticos.append(error_msg)
    else:
        errores_sintacticos.append("Error sintáctico: entrada incompleta")
    
    if len(errores_sintacticos) >= MAX_ERRORES_SINTACTICOS:
        raise SyntaxError("Demasiados errores sintácticos. Se detiene el análisis.")

# Inicializar el analizador
lexer = lex.lex()
parser = yacc.yacc()

# -------- Probar el analizador --------
def analizar_codigo(codigo):
    global errores_lexicos, errores_sintacticos
    errores_lexicos = []
    errores_sintacticos = []
    tabla_tokens = []
    contador_reservadas = 0

    lexer = lex.lex()  # Crear un nuevo lexer
    lexer.lineno = 1   # Asegurarse de que las líneas comienzan en 1

    # Analizar léxicamente el código
    lexer.input(codigo)
    while True:
        tok = lexer.token()
        if not tok:
            break
        es_reservada = 'X' if tok.type in reserved.values() else ''
        es_identificador = 'X' if tok.type == 'ID' else ''

        tabla_tokens.append({
            'Token': tok.value,
            'Reservada': es_reservada,
            'Identificador': es_identificador,
            'Tipo': tok.type,
            'Línea': tok.lineno
        })

        if es_reservada:
            contador_reservadas += 1

    # Analizar sintácticamente el código utilizando el lexer
    parser.parse(codigo, lexer=lexer)

    if not errores_sintacticos:
        errores_sintacticos.append("Errores sintácticos: No se encontraron errores sintácticos.")

    return tabla_tokens, contador_reservadas

# Ruta para servir la página HTML
@app.route('/')
def index():
    return render_template('index1.html')

# Ruta para analizar el código
@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.get_json()
    codigo = data.get('codigo', '')

    # Analizar el código
    tabla_tokens, total_reservadas = analizar_codigo(codigo)

    # Devolver los errores léxicos, sintácticos, tabla de tokens y total de palabras reservadas en formato JSON
    return jsonify({
        'errores_lexicos': errores_lexicos,
        'errores_sintacticos': errores_sintacticos,
        'tabla_tokens': tabla_tokens,
        'total_reservadas': total_reservadas
    })

if __name__ == '__main__':
    app.run(debug=True)
