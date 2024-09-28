import ply.yacc as yacc
from flask import Flask, render_template, request
import re
from analizador_lex import tokens
from token import tokens



app = Flask(__name__)

tokens = (
    'FOR', 'DO', 'WHILE', 'IF', 'ELSE', 'RETURN',
    'INT', 'PUBLIC', 'STATIC', 'VOID', 'FLOAT', 'CHAR', 'STRING',
    'MAIN', 'OUT', 'SYSTEM', 'PRINTLN', 'N', 'LPAREN', 'RPAREN', 
    'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'LE', 'PLUS', 'MINUS', 
    'TIMES', 'DIVIDE', 'ASSIGN', 'SEMICOLON', 'COMMA', 'PERIOD', 'STRING_LITERAL'
)

precedence = (
    ('right', 'FOR', 'DO', 'WHILE', 'IF', 'ELSE', 'RETURN'),  # Palabras reservadas de control de flujo
    ('right', 'INT', 'PUBLIC', 'STATIC', 'VOID'),             # Declaraciones y tipos reservados
    ('right', 'FLOAT', 'CHAR', 'STRING'),                     # Tipos de datos
    ('right', 'MAIN', 'OUT', 'SYSTEM', 'PRINTLN', 'N'),       # Identificadores
    ('left', 'LPAREN', 'RPAREN'),                             # Paréntesis
    ('left', 'LBRACE', 'RBRACE'),                             # Llaves
    ('left', 'LBRACKET', 'RBRACKET'),                         # Corchetes
    ('left', 'LE'),                                           # Comparación (<=)
    ('left', 'PLUS', 'MINUS'),                                # Operadores aritméticos
    ('left', 'TIMES', 'DIVIDE'),                              # Operadores aritméticos
    ('right', 'ASSIGN'),                                      # Operador de asignación (=)
    ('right', 'STRING_LITERAL')                               # Cadenas literales
)



# Reglas para las expresiones binarias (suma, resta, multiplicación, división)
def p_expression_binop(p):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

# Regla para los números
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

# Regla para el uso de paréntesis
def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# Regla para asignaciones
def p_expression_assign(p):
    'expression : IDENTIFIER ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

# Regla para las palabras reservadas
def p_expression_reserved(p):
    '''expression : FOR
                | DO
                | WHILE
                | IF
                | ELSE
                | RETURN'''
    p[0] = p[1]

# Regla para operadores de comparación
def p_expression_comparison(p):
    '''expression : expression LE expression'''
    p[0] = ('<=', p[1], p[3])

# Manejo de errores de sintaxis
#def p_error(p):
#   print("Error de sintaxis en la entrada:", p)

def p_error(p):
    if p:
        print(f"Error de sintaxis en la entrada: {p.value} en la línea {p.lineno}")
    else:
        print("Error de sintaxis: Fin de archivo inesperado")


# Construcción del analizador sintáctico
yacc.yacc()

#/////////////////////////////////////////////////////

# Expresión regular para encontrar tokens
token_regex = r'\w+|[^\w\s]'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['code']
    lines = text.splitlines()
    results = []
    reserved_count = 0
    results = []

    for i, line in enumerate(lines, start=1):
        # Dividir la línea en componentes utilizando expresiones regulares
        tokens_matches = re.finditer(token_regex, line)
        
        for match in tokens_matches:
            token = match.group()
            # Procesar números enteros, descomponiéndolos en dígitos individuales
            if token.isdigit():
                for digit in token:
                    results.append({'token': tokens.get(digit, 'Identificador'), 'lexema': digit, 'linea': i})
            else:
                # Verificar si el token está en el diccionario de tokens, si no, marcarlo como desconocido
                token_type = tokens.get(token, 'Identificador')
                results.append({'token': token_type, 'lexema': token, 'linea': i})
                # Incrementar el contador si es una palabra reservada
                if 'Reservado' == token_type:
                    reserved_count += 1

    return render_template('index.html', results=results, code=text, reserved_count=reserved_count)

if __name__ == '__main__':
    app.run(debug=True)


