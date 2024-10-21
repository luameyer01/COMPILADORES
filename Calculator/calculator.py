from flask import Flask, render_template, request, jsonify
import math
import ply.lex as lex

app = Flask(__name__)

# Definición de los tokens para el analizador léxico
tokens = (
    'NUMERO', 'MAS', 'MENOS', 'POR', 'DIVIDIR', 
    'PAREN_IZQ', 'PAREN_DER'
)

t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIR = r'/'
t_PAREN_IZQ = r'\('
t_PAREN_DER = r'\)'

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

@app.route('/')
def home():
    return render_template('indexCal.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        expresion = request.json['expresion']
        resultado = eval(expresion, {"__builtins__": None}, {"math": math})
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"error": "Expresión inválida"}), 400

@app.route('/analizar', methods=['POST'])
def analizar():
    expresion = request.json['expresion']
    lexer.input(expresion)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({"token": tok.value, "tipo": tok.type})
    return jsonify(tokens)

if __name__ == '__main__':
    app.run(debug=True)
