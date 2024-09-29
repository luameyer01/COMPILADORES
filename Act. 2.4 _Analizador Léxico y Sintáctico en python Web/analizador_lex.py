#Act. 1.3 Práctica . Unidad 1. Realiza un analizador Léxico en python int n=23.2 .-2024
#Ana Gabriela Casanova Hernandez
#Bien

from flask import Flask, render_template, request
import re
#from tokens import tokens#

app = Flask(__name__)




# Definir los tokens
tokens = {
    'for': 'Reservada For',
    'public': 'Reservado',
    'static': 'Reservado',
    'void': 'Reservado',
    'float': 'Tipo Flotante',
    'char': 'Tipo Carácter',
    'string': 'Tipo Cadena',
    'main': 'Identificador',
    'do': 'Reservada Do',
    'while': 'Reservada While',
    'if': 'Reservada If',
    'else': 'Reservada Else',
    'return': 'Reservada Return',
    'int': 'Reservada Int',
    'System': 'Reservado Identificador',
    'out': 'Reservado Identificador',
    'println': 'Reservado Identificador',
    '(': 'Reservada Paren_izq',
    ')': 'Reservada Paren_der',
    '{': 'Reservada Llave_izq',
    '}': 'Reservada Llave_der',
    '=': 'Reservada Igual',
    '+': 'Reservada Suma',
    '1': 'Reservado Numero',
    '5': 'Reservado Numero',
    '<=': 'Reservada Menor Que',  
    ';': 'Reservada Punto_coma',
    '.': 'Reservada Punto',
    '"': 'Reservada Cadena'

}



# Expresión regular para encontrar tokens, incluyendo cadenas y operadores compuestos
token_regex = r'\".*?\"|<=|\w+|[^\w\s]'

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

    for i, line in enumerate(lines, start=1):
        tokens_matches = re.finditer(token_regex, line)

        for match in tokens_matches:
            token = match.group()

            # Si el token es una cadena entre comillas
            if token.startswith('"') and token.endswith('"'):
                token_type = 'Reservada Cadena'
            else:
                token_type = tokens.get(token, 'Identificador')

            results.append({'token': token_type, 'lexema': token, 'linea': i})

            if token_type.startswith('Reservada'):
                reserved_count += 1

        # Detectar error sintáctico si no encuentra ';' al final de la línea
        if not line.endswith(';') and '{' not in line and '}' not in line and line.strip():
            syntax_error = True
            error_lexema = line.strip()  # Guardar la línea con el error
            error_line = i  # Guardar el número de línea del error

    return render_template('index.html', results=results, code=text, reserved_count=reserved_count,
                        syntax_error=syntax_error, error_lexema=error_lexema, error_line=error_line)

if __name__ == '__main__':
    app.run(debug=True)
