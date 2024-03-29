from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from Manager import Manager
from Analizador import Analizador
from xml.etree import ElementTree as ET
from datetime import datetime 

app = Flask(__name__)
CORS(app)
manager = Manager()
lexico = Analizador()

@app.route('/', methods=['GET'])
def principal():
    return 'Arnoldo Luis Antonio González Camey  -  201701548'

@app.route('/agregar_solicitud', methods=['POST'])
def agregar_solicitud():
    xml = request.data.decode('utf-8')
    raiz = ET.XML(xml)
    for elemento in raiz:
        error = False
        error_nit_emisor = 0
        error_nit_receptor = 0
        error_iva = 0
        error_total = 0
        error_referencia = 0
        tiempo = elemento.findtext('TIEMPO').strip()
        dic_tiempo = obtener_fecha_lugar(tiempo)
        lugar = dic_tiempo['lugar']
        fecha = dic_tiempo['fecha']
        hora = dic_tiempo['hora']
        
        if not validar_formato_fecha(fecha):
            error = True
            
        referencia = elemento.findtext('REFERENCIA').strip()
        if manager.existe_referencia(referencia) or not tamano_referencia(referencia):
            error_nit_emisor = 1
            error = True
        
        nit_emisor = elemento.findtext('NIT_EMISOR').strip()
        if not tamano_nit(nit_emisor) or not validar_nit(nit_emisor):
            error_nit_receptor = 1
            error = True
        
        nit_receptor = elemento.findtext('NIT_RECEPTOR').strip()
        if not tamano_nit(nit_receptor) or not validar_nit(nit_receptor):
            error_referencia = 1
            error = True
            
        valor = elemento.findtext('VALOR').strip()
        if not tamano_valor(valor):
            valor = truncate(valor, 2)
        
        iva = elemento.findtext('IVA').strip()
        if not cantidad_iva(float(valor), float(iva)):
            error_iva = 1
            error = True
        
        total = elemento.findtext('TOTAL').strip()
        if not cantidad_total(float(valor), float(total)):
            error_total = 1
            error = True
        
        contador_codigo = manager.obtener_contador_codigo(fecha)
        
        codigo_aprobacion = obtener_codigo_aprobacion(fecha, str(contador_codigo))
        if codigo_aprobacion == 0:
            error = True
            
        if not error:
            manager.añadir_solicitud(codigo_aprobacion, lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total, int(contador_codigo) + 1)
            escribir_archivo(contenido_base_datos(), 'Base_datos', 'Base_Datos')
        else:
            if manager.existe_fecha(fecha):
                manager.modificar_errores_fecha(fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia)
            else:
                manager.añadir_error(fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia)
            
    return jsonify({'agregado': 1,'mensaje':'Archivo XML cargado correctamente :D', 'contenido': xml}), 300

@app.route('/mostrar_solicitudes', methods=['GET'])
def mostrar_solicitudes():
    c = manager.obtener_solicitudes()
    return jsonify(c), 300

@app.route('/reset_autorizaciones', methods=['POST'])
def reset_autorizaciones():
    manager.eliminar_solicitudes()
    escribir_archivo(contenido_base_datos(), 'Base_datos', 'Base_Datos')
    return jsonify({"mensaje":"Solicitudes Eliminadas Exitosamente"}), 300

@app.route('/obtener_datos', methods=['POST'])
def obtener_datos():
    contenido = archivo_salida()
    return jsonify(contenido), 300

@app.route('/obtener_resumen_iva', methods=['POST'])
def obtener_resumen_iva():
    cuerpo = request.get_json()
    fecha = cuerpo['fecha']
    json_receptor = manager.obtener_lista_receptor(fecha)
    json_emisor = manager.obtener_lista_emisor(fecha)
    print(json_receptor)
    print('-------------------')
    print(json_emisor)
    return jsonify({'agregado': 1,'receptor': json_receptor, 'emisor': json_emisor}), 300

@app.route('/rango', methods=['POST'])
def obtener_resumen_iva_rango():
    cuerpo = request.get_json()
    fecha_1 = cuerpo['fecha_1']
    fecha_2 = cuerpo['fecha_2']
    con_iva = cuerpo['con_iva']
    entra = True
    if con_iva == 0:
        entra = True
    else:
        entra = False
    json_rango = manager.obtener_resumen_iva_rango(fecha_1, fecha_2, entra)
    return jsonify(json_rango), 300

@app.route('/guardar_salida', methods=['POST'])
def guardar_salida():
    escribir_archivo(archivo_salida(), 'Autorizaciones', '../Archivo_Salida')
    return jsonify({'exito': 0,'mensaje':'Archivo XML creado correctamente'}), 300

def cargar_base_datos():
    try:
        with open('Base_Datos/Base_datos.xml', 'rt', encoding = 'utf-8') as f:
            print('<<<Base cargada con éxito>>>')
            tree = ET.parse(f)
            root = tree.getroot()
            for elemento in root:
                codigo_aprobacion = elemento.findtext('CODIGO_APROBACION').strip()
                lugar = elemento.findtext('LUGAR').strip()
                fecha = elemento.findtext('FECHA').strip()
                hora = elemento.findtext('HORA').strip()
                referencia = elemento.findtext('REFERENCIA').strip()
                nit_emisor = elemento.findtext('NIT_EMISOR').strip()
                nit_receptor = elemento.findtext('NIT_RECEPTOR').strip()
                valor = elemento.findtext('VALOR').strip()
                iva = elemento.findtext('IVA').strip()
                total = elemento.findtext('TOTAL').strip()
                contador_codigo = elemento.findtext('CONTADOR_CODIGO').strip()
                manager.añadir_solicitud(codigo_aprobacion, lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total, contador_codigo)
    except OSError:
        print("<<<No existe base de datos>>>")
        return

def obtener_codigo_aprobacion(fecha : str, contador_codigo): # tamano total 16 posiciones
    while len(contador_codigo) < 8:
        contador_codigo = '0' + contador_codigo  
    nueva_fecha = fecha.strip().split('/')
    if len(nueva_fecha) == 3:
        codigo_aprobacion = nueva_fecha[2].strip() + nueva_fecha[1].strip() + nueva_fecha[0].strip() + contador_codigo
        return codigo_aprobacion
    return 0   

def tamano_referencia(entrada):
    if len(entrada) <= 40:
        return True
    return False

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

def obtener_fecha_lugar(entrada):
    lexico.analizador_estados(entrada)
    tiempo = lexico.obtener_tokens()
    lexico.reiniciar_tokens()
    return tiempo    

def validar_formato_fecha(fecha):
    try:
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        return False

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

def cantidad_total(valor, total):
    iva = valor*0.12
    dato = round(iva, 2)
    valor = valor + dato
    if valor == total:
        return True
    return False

def truncate(num, n):
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return str(float(temp[:x+n+1]))
            except:
                return temp   
    return temp

def contenido_base_datos():
    contenido = '<AUTORIZADA>'
    solicitudes = manager.obtener_solicitudes()
    for i in range(len(solicitudes)):
        contenido += '''
    <DTE>
        <CODIGO_APROBACION>'''+solicitudes[i]['codigo_aprobacion']+'''</CODIGO_APROBACION>
        <LUGAR>'''+solicitudes[i]['lugar']+'''</LUGAR>
        <FECHA>'''+solicitudes[i]['fecha']+'''</FECHA>
        <HORA>'''+solicitudes[i]['hora']+'''</HORA>
        <REFERENCIA>'''+solicitudes[i]['referencia']+'''</REFERENCIA>
        <NIT_EMISOR>'''+solicitudes[i]['nit_emisor']+'''</NIT_EMISOR>
        <NIT_RECEPTOR>'''+solicitudes[i]['nit_receptor']+'''</NIT_RECEPTOR>
        <VALOR>'''+solicitudes[i]['valor']+'''</VALOR>
        <IVA>'''+solicitudes[i]['iva']+'''</IVA>
        <TOTAL>'''+solicitudes[i]['total']+'''</TOTAL>
        <CONTADOR_CODIGO>'''+str(solicitudes[i]['contador_codigo'])+'''</CONTADOR_CODIGO>
    </DTE>'''
    contenido +='\n</AUTORIZADA>'
    return contenido

def archivo_salida():
    fechas = manager.guardar_fecha_solicitud()
    fechas.sort(key = lambda date: datetime.strptime(date, '%d/%m/%Y')) 
    contenido = '<LISTAAUTORIZACIONES>'
    for fecha in fechas:
        cant_facturas_correctas = manager.cantidad_facturas_fecha(fecha)
        cant_facturas_error= manager.cantidad_facturas_fecha_error(fecha)
        contenido += '''
    <AUTORIZACION>
        <FECHA>'''+fecha+'''</FECHA>
        <FACTURAS_RECIBIDAS>'''+str(cant_facturas_correctas + cant_facturas_error)+'''</FACTURAS_RECIBIDAS>'''
        contenido += archivo_salida_error(fecha)
        contenido += '''
        <FACTURAS_CORRECTAS>'''+str(cant_facturas_correctas)+'''</FACTURAS_CORRECTAS>
        <CANTIDAD_EMISORES>'''+manager.obtener_num_emisor(fecha)+'''</CANTIDAD_EMISORES>
        <CANTIDAD_RECEPTORES>'''+manager.obtener_num_receptor(fecha)+'''</CANTIDAD_RECEPTORES>'''
        contenido += archivo_salida_listado_autorizaciones(fecha) + '\n'
        contenido += '\t</AUTORIZACION>'
        
    contenido +='\n</LISTAAUTORIZACIONES>'
    return contenido

def archivo_salida_listado_autorizaciones(fecha):
    contenido = '\n\t\t<LISTADO_AUTORIZACIONES>'
    solicitudes = manager.obtener_solicitudes()
    for i in range(len(solicitudes)):
        if solicitudes[i]['fecha'] == fecha:
            contenido += '''
            <APROBACION>
                <NIT_EMISOR ref="'''+solicitudes[i]['referencia']+'''">'''+solicitudes[i]['nit_emisor']+'''</NIT_EMISOR>
                <CODIGO_APROBACION>'''+solicitudes[i]['codigo_aprobacion']+'''</CODIGO_APROBACION>
                <NIT_RECEPTOR>'''+solicitudes[i]['nit_receptor']+'''</NIT_RECEPTOR>
                <VALOR>'''+solicitudes[i]['valor']+'''</VALOR>
            </APROBACION>'''
    contenido += '\n\t\t</LISTADO_AUTORIZACIONES>'
    return contenido

def archivo_salida_error(fecha):
    contenido = ''
    errores = manager.obtener_errores()
    for i in range(len(errores)):
        if errores[i]['fecha'] == fecha:
            contenido += '''
            <ERRORES>
                <NIT_EMISOR>'''+str(errores[i]['error_nit_emisor'])+'''</NIT_EMISOR>
                <NIT_RECEPTOR>'''+str(errores[i]['error_nit_receptor'])+'''</NIT_RECEPTOR>
                <IVA>'''+str(errores[i]['error_iva'])+'''</IVA>
                <TOTAL>'''+str(errores[i]['error_total'])+'''</TOTAL>
                <REFERENCIA_DUPLICADA>'''+str(errores[i]['error_referencia'])+'''</REFERENCIA_DUPLICADA>
            </ERRORES>'''
    return contenido

def escribir_archivo(contenido_xml, nombre_archivo, url_carpeta):
    os.makedirs(url_carpeta, exist_ok = True)
    miArchivo = open(url_carpeta+'/'+nombre_archivo + '.xml','w')
    miArchivo.write(contenido_xml)
    miArchivo.close()
    print('Se generó el archivo correctamente')              

if __name__ == '__main__':
    cargar_base_datos()
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host = 'localhost', port = puerto)  
    escribir_archivo(archivo_salida(), 'salida', 'Base_Datos')