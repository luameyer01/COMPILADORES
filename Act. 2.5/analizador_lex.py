#Act. 1.3 Práctica . Unidad 1. Realiza un analizador Léxico en python int n=23.2 .-2024
#Ana Gabriela Casanova Hernandez
#Bien
from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Definir los tokens basados en tu tabla
tokens = {
    'programa': 'Reservado Programa',
    'int': 'Reservado Int',
    'read': 'Reservado Read',
    'for': 'Reservado For',
    'public': 'Reservado Public',
    'static': 'Reservado Static',
    'void': 'Reservado Void',
    'float': 'Reservado Float',
    'char': 'Reservado Char',
    'string': 'Reservado Cadena',
    'main': 'Identificador Main',
    'do': 'Reservado Do',
    'while': 'Reservado While',
    'if': 'Reservado If',
    'else': 'Reservado Else',
    'return': 'Reservado Return',
    'System': 'Identificador System',
    'out': 'Identificador Out',
    'println': 'Identificador Println',

    '(': 'Delimitador Paren_izq',
    ')': 'Delimitador Paren_der',
    '{': 'Delimitador Llave_izq',
    '}': 'Delimitador Llave_der',
    '=': 'Símbolo Igual',
    '+': 'Símbolo Suma',
    '++': 'Símbolo Incremento',
    '<=': 'Símbolo Menor_que',
    ';': 'Delimitador Punto_coma',
    '.': 'Símbolo Punto',
    '"': 'Delimitador Comillas',
    'a': 'Identificador a',
    'b': 'Identificador b',
    'c': 'Identificador c'
}

# Expresión regular para encontrar tokens, incluyendo cadenas, números, identificadores y operadores compuestos
token_regex = r'\".*?\"|<=|\+\+|\d+|\w+|[^\w\s]'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['code']
    lines = text.splitlines()
    results = []
    reserved_count = 0
    syntax_error = False
    error_lexema = None
    error_line = None
    error_position = None
    lex_error = False

    for i, line in enumerate(lines, start=1):
        tokens_matches = re.finditer(token_regex, line)

        for match in tokens_matches:
            token = match.group()
            position = match.start() + 1  # Posición del carácter en la línea

            if token.startswith('"') and token.endswith('"'):
                token_type = 'Delimitador Cadena'
            elif token.isdigit():
                token_type = 'Número'  # Cualquier número
            elif re.match(r'^[a-zA-Z_]\w*$', token) and token not in tokens:
                token_type = 'Identificador'  # Cualquier identificador que no sea una palabra reservada
            else:
                token_type = tokens.get(token, None)

            if token_type:
                results.append({'token': token_type, 'lexema': token, 'linea': i})
                if token_type.startswith('Reservado'):
                    reserved_count += 1
            else:
                # Marcar un error léxico si no coincide con ningún token
                lex_error = True
                error_lexema = token
                error_line = i
                error_position = position
                break

        # Si hay un error léxico, detener el análisis
        if lex_error:
            break

        # Detectar error sintáctico si no encuentra ';' al final de la línea
        if not line.endswith(';') and '{' not in line and '}' not in line and line.strip() and not lex_error:
            syntax_error = True
            error_lexema = line.strip()
            error_line = i
            break

    if lex_error:
        error_message = f"ERROR EN LA LÍNEA {error_line}, POSICIÓN {error_position}: CARACTER NO VÁLIDO '{error_lexema}'"
    elif syntax_error:
        error_message = f"ERROR DE SINTAXIS EN LA LÍNEA {error_line}. SE ESPERABA UNA EXPRESIÓN VÁLIDA."
    else:
        error_message = "NO HAY ERRORES DE SINTAXIS"

    return render_template('index.html', results=results, code=text, reserved_count=reserved_count,
                           syntax_error=syntax_error, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
