#Act. 1.3 Práctica . Unidad 1. Realiza un analizador Léxico en python int n=23.2 .-2024
#Ana Gabriela Casanova Hernandez
#Bien

from flask import Flask, render_template, request
import re
#from tokens import tokens#

app = Flask(__name__)

# Expresión regular para encontrar tokens
token_regex = r'\w+|[^\w\s]'

# Tu código del analizador


# Definir los tokens
tokens = {
    'FOR': 'Reservado',
    'DO': 'Reservado',
    'WHILE': 'Reservado',
    'IF': 'Reservado',
    'ELSE': 'Reservado',
    'RETURN': 'Reservado',
    'INT': 'Declaracion',
    'PUBLIC': 'Declaracion',
    'STATIC': 'Declaracion',
    'VOID': 'Declaracion',
    'FLOAT': 'TipoDato',
    'CHAR': 'TipoDato',
    'STRING': 'TipoDato',
    'MAIN': 'Identificador',
    'OUT': 'Identificador',
    'SYSTEM': 'Identificador',
    'PRINTLN': 'Identificador',
    'N': 'Identificador',
    'LPAREN': 'Parentesis',
    'RPAREN': 'Parentesis',
    'LBRACE': 'Llave',
    'RBRACE': 'Llave',
    'LBRACKET': 'Corchete',
    'RBRACKET': 'Corchete',
    'LE': 'Comparacion',
    'PLUS': 'Operador',
    'MINUS': 'Operador',
    'TIMES': 'Operador',
    'DIVIDE': 'Operador',
    'ASSIGN': 'Asignacion',
    'SEMICOLON': 'Puntuacion',
    'COMMA': 'Puntuacion',
    'PERIOD': 'Puntuacion',
    'STRING_LITERAL': 'CadenaLiteral',
    'NUMBER': 'Numero',
    'IDENTIFIER': 'Identificador'
}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['code']
    lines = text.splitlines()
    results = []
    reserved_count = 0

    for i, line in enumerate(lines, start=1):
        tokens_matches = re.finditer(r'\w+|[^\w\s]', line)
        
        for match in tokens_matches:
            token = match.group()
            if token.isdigit():
                results.append({'token': 'Numero', 'lexema': token, 'linea': i})
            else:
                token_type = tokens.get(token, 'Desconocido')
                results.append({'token': token_type, 'lexema': token, 'linea': i})

            if 'Reservado' == token_type:
                reserved_count += 1

    return render_template('index.html', results=results, code=text, reserved_count=reserved_count)

if __name__ == '__main__':
    app.run(debug=True)
