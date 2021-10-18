from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from Manager import Manager
from xml.etree import ElementTree as ET

app = Flask(__name__)
CORS(app)
manager = Manager()

@app.route('/', methods=['GET'])
def principal():
    return 'Arnoldo Luis Antonio González Camey  -  201701548'

@app.route('/agregar_solicitud', methods=['POST'])
def agregar_solicitud():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        tiempo = elemento.findtext('TIEMPO').strip()
        dic_tiempo = obtener_fecha_lugar(tiempo)
        lugar = dic_tiempo['lugar']
        fecha = dic_tiempo['fecha']
        hora = dic_tiempo['hora']
        
        referencia = elemento.findtext('REFERENCIA').strip()
        if manager.existe_referencia(referencia):
            return jsonify({'agregado': 0,'mensaje':'Error la referencia enviada ya existe'}), 300
        
        nit_emisor = elemento.findtext('NIT_EMISOR').strip()
        if not tamano_nit(nit_emisor):
            return jsonify({'agre gado': 0,'mensaje':'Error ingreso NIT Emisor'}), 300
        if not validar_nit(nit_emisor):
            return jsonify({'agregado': 0,'mensaje':'NIT Emisor inválido'+nit_emisor}), 300
        
        nit_receptor = elemento.findtext('NIT_RECEPTOR').strip()
        if not tamano_nit(nit_receptor):
            return jsonify({'agregado': 0,'mensaje':'Error ingreso NIT Receptor'}), 300
        if not validar_nit(nit_receptor):
            return jsonify({'agregado': 0,'mensaje':'NIT Receptor inválido'+nit_receptor}), 300
        
        valor = elemento.findtext('VALOR').strip()
        if not tamano_valor(float(valor)):
            return jsonify({'agregado': 0,'mensaje':'Error ingreso Valor'}), 300
        
        iva = elemento.findtext('IVA').strip()
        if not cantidad_iva(valor, float(iva)):
            return jsonify({'agregado': 0,'mensaje':'Error ingreso IVA'}), 300
        
        total = elemento.findtext('TOTAL').strip()
        if not cantidad_total(valor, iva, float(total)):
            return jsonify({'agregado': 0,'mensaje':'Error ingreso Total'}), 300
        
        manager.añadir_solicitud(lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total)
    return jsonify({'agregado': 1,'mensaje':'Archivo XML cargado correctamente :D'}), 300

@app.route('/mostrar_solicitudes', methods=['GET'])
def get_characters():
    c = manager.obtener_solicitudes()
    return jsonify(c), 300

def validar_nit(entrada):
    suma = 0
    entrada = str(entrada)
    for i in range(len(entrada)):
        posicion = len(entrada) - i
        actual = entrada[i]
        num = int(actual) * posicion #paso 1 -> multiplicación de la posición y el numero
        if posicion != 1:
            suma += num  #paso 2 -> suma de las multiplicaciones
    modulo_suma = suma % 11 #paso 3 -> suma modulo 11
    resta_mod = 11 - modulo_suma #paso 4 -> 11 menos el modulo anterior
    modulo_k = resta_mod % 11 #paso 5 -> resta modulo 11 : k
    if modulo_k < 10 and modulo_k == int(entrada[len(entrada) - 1]): #paso 6 k < 10 Y k == V
        return True
    return False
# 2 4 2 8 4 9 5 5 --> NIT         3 9 8 8 8 3 2 0
# 8 7 6 5 4 3 2 1 --> POSICION    8 7 6 5 4 3 2 1

def obtener_fecha_lugar(entrada : str):
    entrada = entrada.split(',')
    lugar = entrada[0].strip()
    resto = entrada[1].strip().split(' ', maxsplit = 1)
    fecha = resto[0].strip()
    hora = resto[1].strip()
    tiempo = {'lugar':lugar, 'fecha':fecha, 'hora':hora}
    return tiempo   

def tamano_nit(entrada):
    if len(str(entrada)) <= 20:
        return True
    return False

def tamano_valor(entrada):
    entrada = str(entrada).split('.')
    if len(entrada) > 1:
        if len(entrada[1]) == 2:
            return True
    return False

def cantidad_iva(valor, iva):
    dato = valor*0.12
    dato = round(dato, 2)
    if dato == iva:
        return True
    return False

def cantidad_total(valor, iva, total):
    valor = valor + iva
    if valor == total:
            return True
    return False

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host = 'localhost', port = puerto)  