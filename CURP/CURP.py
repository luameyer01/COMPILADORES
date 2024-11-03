from flask import Flask, render_template, request

app = Flask(__name__)

class CurpAnalyzer:
    estados = {
        "AS": "AGUASCALIENTES", "BC": "BAJA CALIFORNIA", "BS": "BAJA CALIFORNIA SUR",
        "CC": "CAMPECHE", "CL": "COAHUILA", "CM": "COLIMA", "CS": "CHIAPAS",
        "CH": "CHIHUAHUA", "DF": "CIUDAD DE MÉXICO", "DG": "DURANGO", "GT": "GUANAJUATO",
        "GR": "GUERRERO", "HG": "HIDALGO", "JC": "JALISCO", "MC": "MÉXICO",
        "MN": "MICHOACÁN", "MS": "MORELOS", "NT": "NAYARIT", "NL": "NUEVO LEÓN",
        "OC": "OAXACA", "PL": "PUEBLA", "QT": "QUERÉTARO", "QR": "QUINTANA ROO",
        "SP": "SAN LUIS POTOSÍ", "SL": "SINALOA", "SR": "SONORA", "TC": "TABASCO",
        "TS": "TAMAULIPAS", "TL": "TLAXCALA", "VZ": "VERACRUZ", "YN": "YUCATÁN",
        "ZS": "ZACATECAS", "NE": "NACIDO EN EL EXTRANJERO"
    }
    valores = {
        **{str(i): i for i in range(10)},  # '0' a '9'
        **{chr(i): i - 55 for i in range(65, 91)}  # 'A' a 'Z', donde A=10, B=11, ..., Z=35
    }
    iniciales_inapropiadas = ["BUEI", "CACA", "CAGA", "CAGO", "CAKA", "CAKO", 
                              "COGE", "COJA", "COJE", "COJI", "COJO", "CULO", 
                              "FETO", "GUEY", "JOTO", "KACA", "KACO", "KAGA", 
                              "KAGO", "KOGE", "KOJO", "KAKA", "KULO", "MAME", 
                              "MAMO", "MEAR", "MEAS", "MEON", "MION", "MOCO", 
                              "MULA", "PEDA", "PEDO", "PENE", "PUTA", "PUTO", 
                              "QULO", "RATA", "RUIN"]

    def __init__(self, nombre, primer_apellido, segundo_apellido, dia, mes, anio, sexo, estado):
        self.nombre = nombre.upper()
        self.primer_apellido = primer_apellido.upper()
        self.segundo_apellido = segundo_apellido.upper() if segundo_apellido else "X"
        self.dia = dia.zfill(2)
        self.mes = mes.zfill(2)
        self.anio = anio[-2:]
        self.sexo = sexo.upper()
        self.estado = estado

    def generate_curp(self):
        # Construcción de la CURP base sin homonimia y dígito verificador
        curp_base = (
            self.get_first_letter(self.primer_apellido) +
            self.get_first_vowel(self.primer_apellido) +
            self.get_first_letter(self.segundo_apellido) +
            self.get_first_letter(self.nombre) +
            self.anio +
            self.mes +
            self.dia +
            self.sexo +
            self.estado +
            self.get_internal_consonant(self.primer_apellido) +
            self.get_internal_consonant(self.segundo_apellido) +
            self.get_internal_consonant(self.nombre)
        )

        # Calcular homonimia y dígito verificador
        homonimia = self.calcular_homonimia()
        curp_con_homonimia = curp_base + str(homonimia)
        curp_con_homonimia = self.validar_homoclave(curp_con_homonimia)  # Validación de homoclave
        digito_verificador = self.calcular_digito_verificador(curp_con_homonimia)

        # Concatenar CURP completa
        curp_completa = curp_con_homonimia + str(digito_verificador)
        return curp_completa

    def get_first_letter(self, word):
        return "X" if word[0] == "Ñ" else word[0]

    def get_first_vowel(self, word):
        for char in word[1:]:
            if char in "AEIOU":
                return char
        return "X"

    def get_internal_consonant(self, word):
        for char in word[1:]:
            if char in "BCDFGHJKLMNÑPQRSTVWXYZ":
                return char
        return "X"

    def calcular_homonimia(self):
        tabla_valores = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
            'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'Ñ': 15,
            'O': 16, 'P': 17, 'Q': 18, 'R': 19, 'S': 20, 'T': 21, 'U': 22,
            'V': 23, 'W': 24, 'X': 25, 'Y': 26, 'Z': 27
        }
        cadena = self.primer_apellido + self.segundo_apellido + self.nombre
        valor_total = sum(tabla_valores.get(letra.upper(), 0) for letra in cadena)
        return valor_total % 10  # Se toma el módulo 10 del valor

    def calcular_digito_verificador(self, curp_sin_dv):
        factores = [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        try:
            suma = sum(self.valores[digito] * factor for digito, factor in zip(curp_sin_dv, factores))
            return (10 - (suma % 10)) % 10
        except KeyError as e:
            print(f"Error: Carácter no válido encontrado en CURP sin dígito verificador: {e}")
            raise ValueError("CURP contiene caracteres no válidos para el cálculo del dígito verificador.")

    def validar_homoclave(self, curp):
        homoclave = curp[:4]
        if homoclave in self.iniciales_inapropiadas:
            curp = homoclave[0] + "X" + homoclave[2:] + curp[4:]
        return curp

    def analyze(self):
        curp = self.generate_curp()
        return f"CURP generada: {curp}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        primer_apellido = request.form.get('primer_apellido')
        segundo_apellido = request.form.get('segundo_apellido')
        dia = request.form.get('dia')
        mes = request.form.get('mes')
        anio = request.form.get('anio')
        sexo = request.form.get('sexo')
        estado = request.form.get('estado')

        if nombre and primer_apellido and dia and mes and anio and sexo and estado:
            analyzer = CurpAnalyzer(nombre, primer_apellido, segundo_apellido, dia, mes, anio, sexo, estado)
            result = analyzer.analyze()
        else:
            result = "Por favor, completa todos los campos obligatorios."

    return render_template('CURP.html', result=result, estados=CurpAnalyzer.estados)

if __name__ == '__main__':
    app.run(debug=True)
