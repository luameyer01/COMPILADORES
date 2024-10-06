from flask import Flask, request, jsonify, render_template
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# ------------- Analizador léxico -------------
tokens = [
    'PROGRAMA', 'INT', 'ID', 'READ', 'PRINTF', 'PUNTOCOMA', 'PARENTESIS_ABIERTO', 'PARENTESIS_CERRADO', 'STRING', 'COMA', 'IGUAL', 'LLAVE_ABIERTA', 'LLAVE_CERRADA', 'END', 'MAS'
]

t_MAS = r'\+'
t_PUNTOCOMA = r'\;'
t_COMA = r'\,'
t_IGUAL = r'='
t_PARENTESIS_ABIERTO = r'\('
t_PARENTESIS_CERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'
t_ignore = ' \t'

# Palabras clave
reserved = {
    'int': 'INT',
    'read': 'READ',
    'printf': 'PRINTF',
    'end': 'END',
    'programa': 'PROGRAMA'
}

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

# Definir reglas gramaticales
def p_program(p):
    '''programa : ID ID PARENTESIS_ABIERTO  PRINTF PARENTESIS_CERRADO  LLAVE_ABIERTA  declaration statements END PUNTOCOMA LLAVE_CERRADA'''
    '''programa: ID ID PARENTESIS_ABIERTO  PARENTESIS_CERRADO  LLAVE_ABIERTA  declaration statements LLAVE_CERRADA
            | ID ID PARENTESIS_ABIERTO PRINTF PARENTESIS_CERRADO  LLAVE_ABIERTA  declaration statements END PUNTOCOMA LLAVE_CERRADA'''
    print("Fin del programa detectado correctamente.")

def p_declaration(p):
    '''declaration : INT varlist PUNTOCOMA'''
    pass

def p_varlist(p):
    '''varlist : ID
            | ID COMA varlist'''
    pass

def p_statements(p):
    '''statements : statement statements
                | statement'''
    pass

def p_statement_read(p):
    '''statement : READ ID PUNTOCOMA'''
    pass

def p_statement_printf(p):
    '''statement : PRINTF PARENTESIS_ABIERTO STRING PARENTESIS_CERRADO PUNTOCOMA
                | PRINTF PARENTESIS_ABIERTO ID PARENTESIS_CERRADO PUNTOCOMA'''
    pass


def p_statement_assign(p):
    '''statement : ID IGUAL expression PUNTOCOMA'''
    pass

def p_expression(p):
    '''expression : ID MAS ID'''
    pass

# Manejo de errores sintácticos
def p_error(p):
    if p:
        error_msg = f"Error sintáctico en '{p.value}' en la línea {p.lineno}"
        errores_sintacticos.append(error_msg)
    else:
        errores_sintacticos.append("Error sintáctico: entrada incompleta")

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
    
    # Reiniciar el contador de líneas antes de analizar el nuevo código
    lexer.lineno = 1  # Reiniciar el contador de líneas

    # Analizar léxicamente el código
    lexer.input(codigo)
    while True:
        tok = lexer.token()
        if not tok:
            break
        # Determinar si es una palabra reservada o identificador
        es_reservada = 'X' if tok.type in reserved.values() else ''
        es_identificador = 'X' if tok.type == 'ID' else ''
        
        # Añadir a la tabla
        tabla_tokens.append({
            'Token': tok.value,
            'Reservada': 'X' if tok.type == 'PROGRAMA' else es_reservada,  # Modificación aquí
            'Identificador': es_identificador,
            'Tipo': tok.type,
            'Línea': tok.lineno
        })

        # Contar palabras reservadas
        if es_reservada:
            contador_reservadas += 1
    
    # Analizar sintácticamente el código
    parser.parse(codigo)
    
    # Devolver los resultados, incluyendo la tabla de tokens y el conteo de reservadas
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
