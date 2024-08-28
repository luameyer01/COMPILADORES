#Act. 1.3 Práctica . Unidad 1. Realiza un analizador Léxico en python int n=23.2 .-2024
#Ana Gabriela Casanova Hernandez
#Bien

from flask import Flask, render_template, request
import re

app = Flask(__name__)


# Definir los tokens
tokens = {
    'for': 'Reservada For',
    'do': 'Reservada Do',
    'while': 'Reservada While',
    'if': 'Reservada If',
    'else': 'Reservada Else',
    'return': 'Reservada Return',
    'int': 'Reservado',
    'public': 'Reservado',
    'static': 'Reservado',
    'void': 'Reservado',
    'float': 'Tipo Flotante',
    'char': 'Tipo Carácter',
    'string': 'Tipo Cadena',
    'main': 'Identificador',
    'n': 'Identificador',
    '(': 'Delimitador',
    ')': 'Delimitador',
    '{': 'Delimitador',
    '}': 'Delimitador',
    '0': 'Entero',
    '1': 'Entero',
    '2': 'Entero',
    '3': 'Entero',
    '4': 'Entero',
    '5': 'Entero',
    '6': 'Entero',
    '7': 'Entero',
    '8': 'Entero',
    '9': 'Entero',
    ';': 'Simbolo',
    '.': 'Simbolo',
    '[': 'Simbolo',
    ']': 'simbolo',
    ',': 'simbolo',
    '+': 'Operador de suma',
    '-': 'Operador de resta',
    '*': 'Operador de multiplicación',
    '/': 'Operador de división',
    '=': 'Operador',
}

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
