import ply.yacc as yacc
from flask import Flask, render_template, request
import re

from analizador_lex import tokens  # Asegúrate de que este archivo tenga los tokens del analizador léxico.

# Definimos los tokens que se utilizarán en el analizador sintáctico.
tokens = [
    'FOR', 'PUBLIC', 'STATIC', 'VOID', 'FLOAT', 'CHAR', 'STRING', 'MAIN', 'DO', 'WHILE', 
    'IF', 'ELSE', 'RETURN', 'INT', 'SYSTEM', 'OUT', 'PRINTLN', 'PAREN_IZQ', 'PAREN_DER', 
    'LLAVE_IZQ', 'LLAVE_DER', 'IGUAL', 'SUMA', 'INCREMENTO', 'MENOR_QUE', 'PUNTO_COMA', 
    'PUNTO', 'CADENA', 'NUMERO', 'IDENTIFICADOR'
]

# Precedencia de operadores
precedence = (
    ('right', 'FOR', 'DO', 'WHILE', 'IF', 'ELSE', 'RETURN'),  
    ('right', 'INT', 'PUBLIC', 'STATIC', 'VOID'),  
    ('right', 'FLOAT', 'CHAR', 'STRING'),  
    ('right', 'MAIN', 'OUT', 'SYSTEM', 'PRINTLN', 'N'),  
    ('left', 'LPAREN', 'RPAREN'),  
    ('left', 'LBRACE', 'RBRACE'),  
    ('left', 'LE'),  
    ('left', 'PLUS', 'MINUS'),  
    ('left', 'TIMES', 'DIVIDE'),  
    ('right', 'ASSIGN'),  
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ASSIGN'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'LE'),
    ('right', 'STRING_LITERAL')  
)


# Expresión regular para encontrar tokens, incluyendo cadenas, números, identificadores y operadores compuestos
token_regex = r'\".*?\"|<=|\+\+|\d+|\w+|[^\w\s]'


# Reglas para expresiones binarias
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

# Regla para números
def p_expression_number(p):
    'expression : N'
    p[0] = p[1]

# Regla para paréntesis
def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# Regla para asignaciones
def p_expression_assign(p):
    'expression : OUT ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

# Regla para palabras reservadas
def p_expression_reserved(p):
    '''expression : FOR
                  | DO
                  | WHILE
                  | IF
                  | ELSE
                  | RETURN'''
    p[0] = p[1]

# Regla para comparación
def p_expression_comparison(p):
    'expression : expression LE expression'
    p[0] = ('<=', p[1], p[3])

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis: Fin de archivo inesperado")

# Construcción del parser
parser = yacc.yacc()

# Código Flask y análisis
app = Flask(__name__)

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
        tokens_matches = re.finditer(token_regex, line)
        
        for match in tokens_matches:
            token = match.group()
            if token.isdigit():
                for digit in token:
                    results.append({'token': tokens.get(digit, 'Identificador'), 'lexema': digit, 'linea': i})
            else:
                token_type = tokens.get(token, 'Identificador')
                results.append({'token': token_type, 'lexema': token, 'linea': i})
                if 'Reservado' == token_type:
                    reserved_count += 1

    return render_template('index.html', results=results, code=text, reserved_count=reserved_count)

if __name__ == '__main__':
    app.run(debug=True)
