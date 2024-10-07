from flask import Flask, request, jsonify, render_template
import ply.lex as lex
import ply.yacc as yacc
import re  # Importamos el módulo re para el manejo de expresiones regulares

app = Flask(__name__)

# ------------- Analizador léxico -------------
tokens = [
    'PROGRAMA', 'INT', 'ID', 'READ', 'PRINTF', 'PUNTOCOMA', 'PARENTESIS_ABIERTO', 'PARENTESIS_CERRADO',
    'STRING', 'COMA', 'IGUAL', 'LLAVE_ABIERTA', 'LLAVE_CERRADA', 'END', 'MAS'
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
variables_declaradas = set()  # Aquí almacenamos las variables declaradas
int_declared = False  # Bandera para verificar si se ha declarado 'int'

# Definir reglas gramaticales
def p_program(p):
    '''programa : PROGRAMA ID PARENTESIS_ABIERTO PARENTESIS_CERRADO LLAVE_ABIERTA declaration statements END PUNTOCOMA LLAVE_CERRADA'''
    pass

def p_declaration(p):
    '''declaration : INT varlist PUNTOCOMA'''
    global int_declared
    int_declared = True
    for var in p[2]:  # Suponiendo que varlist retorna una lista de variables
        variables_declaradas.add(var)

def p_varlist(p):
    '''varlist : ID
            | ID COMA varlist'''
    if len(p) == 2:
        p[0] = [p[1]]  # Solo una variable
    else:
        p[0] = [p[1]] + p[3]  # Lista de variables

def p_statements(p):
    '''statements : statement statements
                | statement'''
    pass

def p_statement_read(p):
    '''statement : READ ID PUNTOCOMA'''
    if p[2] not in variables_declaradas:
        errores_sintacticos.append(f"Error de sintaxis. Variable no definida: '{p[2]}'")
    pass

def p_statement_printf(p):
    '''statement : PRINTF PARENTESIS_ABIERTO STRING PARENTESIS_CERRADO
                | PRINTF PARENTESIS_ABIERTO ID PARENTESIS_CERRADO'''
    pass

def p_statement_assign(p):
    '''statement : ID IGUAL expression PUNTOCOMA'''
    if p[1] not in variables_declaradas:
        errores_sintacticos.append(f"Error de sintaxis. Variable no definida: '{p[1]}'")
    pass

def p_expression(p):
    '''expression : ID MAS ID'''
    if p[1] not in variables_declaradas:
        errores_sintacticos.append(f"Error de sintaxis. Variable no definida: '{p[1]}'")
    if p[3] not in variables_declaradas:
        errores_sintacticos.append(f"Error de sintaxis. Variable no definida: '{p[3]}'")
    pass

# Manejo de errores sintácticos
# Limitar la cantidad de errores que se pueden agregar a la lista de errores sintácticos
MAX_ERRORES_SINTACTICOS = 6

def p_error(p):
    if len(errores_sintacticos) >= MAX_ERRORES_SINTACTICOS:
        return

    if p:
        error_msg = f"Error sintáctico en '{p.value}' en la línea {p.lineno}"
        errores_sintacticos.append(error_msg)
    else:
        errores_sintacticos.append("Error sintáctico: entrada incompleta")
    
    # Detener el parser si se alcanzó el límite de errores
    if len(errores_sintacticos) >= MAX_ERRORES_SINTACTICOS:
        raise SyntaxError("Demasiados errores sintácticos. Se detiene el análisis.")


# Verificaciones adicionales para la estructura del código
def verificar_estructura(codigo):
    global errores_sintacticos
    syntax_errors = []
    declared_variables = set()
    int_declared = False

    lines = codigo.splitlines()

    # 1. Verificar la llave de inicio '{' solo en la primera línea
    if lines and '{' not in lines[0]:
        syntax_errors.append("Error de sintaxis: Falta la llave de inicio '{' al inicio del bloque.")

    # 2. Verificar la llave de cierre '}' solo en la última línea
    if lines and '}' not in lines[-1]:
        syntax_errors.append("Error de sintaxis: Falta la llave de cierre '}' al final del bloque.")

    # Recorrer las líneas de código para otros errores
    for i, line in enumerate(lines):
        if 'int' in line:
            int_declared = True
            declared_vars = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', line)
            declared_variables.update(declared_vars)

        # Verificar uso de variables no declaradas en read
        if 'read' in line:
            variable = re.search(r'read\s+(\w+)', line)
            if variable and variable.group(1) not in declared_variables:
                syntax_errors.append(f"Error: identificador '{variable.group(1)}' en la instrucción 'read' no declarado.")

        # Verificar operación de suma
        if '=' in line:
            left_side = line.split('=')[0]
            if '+' in left_side:
                operands = re.split(r'\s*\+\s*', left_side)
                for operand in operands:
                    operand = operand.strip()
                    if not (re.match(r'^\d+$', operand) or operand in declared_variables):
                        syntax_errors.append(f"Error de sintaxis en la línea {i+1}: Token inesperado '+'.")
                        break

    if not int_declared:
        syntax_errors.append("Error: palabra reservada 'int' no declarada.")
    
    return syntax_errors

# Inicializar el analizador
lexer = lex.lex()
parser = yacc.yacc()

# -------- Probar el analizador --------
def analizar_codigo(codigo):
    global errores_lexicos, errores_sintacticos, variables_declaradas
    errores_lexicos = []
    errores_sintacticos = []
    variables_declaradas = set()
    tabla_tokens = []
    contador_reservadas = 0

    lexer.lineno = 1

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
            'Reservada': 'X' if tok.type == 'PROGRAMA' else es_reservada,
            'Identificador': es_identificador,
            'Tipo': tok.type,
            'Línea': tok.lineno
        })

        if es_reservada:
            contador_reservadas += 1

    # Analizar sintácticamente el código
    parser.parse(codigo)

    # Verificar estructura del código
    errores_sintacticos.extend(verificar_estructura(codigo))

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
