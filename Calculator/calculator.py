from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('indexCal.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        expresion = request.json['expresion']
        # Evaluar la expresión de forma segura utilizando eval restringido
        resultado = eval(expresion, {"__builtins__": None}, {"math": math})
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"error": "Expresión inválida"}), 400

if __name__ == '__main__':
    app.run(debug=True)
