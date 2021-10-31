from DTE import DTE
from Error import Error

class Manager():
    def __init__(self):
        self.solicitudes = []
        self.errores = []

    #----------------------------------SOLICITUD----------------------------------------------
    
    def añadir_solicitud(self, codigo_aprobacion, lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total, contador_codigo):
        nuevo_dte = DTE(codigo_aprobacion, lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total, contador_codigo)
        self.solicitudes.append(nuevo_dte)
        return True
    
    def get_tamano_solicitud(self):
        return str(len(self.solicitudes))
    
    def obtener_solicitudes(self):
        json_solicitudes = []
        for requests in self.solicitudes:
            json_solicitudes.append(requests.get_json())
        return json_solicitudes
    
    def obtener_contador_codigo(self, fecha):
        nuevo_contador = 1
        for requests in self.solicitudes:
            if requests.fecha == fecha:
                nuevo_contador = requests.contador_codigo
        return nuevo_contador
            
    def existe_referencia(self, referencia):
        for requests in self.solicitudes:
            if requests.referencia == referencia:
                return True
        return False  
    
    def existe_fecha_solicitud(self, fecha, fechas):
        for f in fechas:
            if f == fecha:
                return True
        return False 
    
    def guardar_fecha_solicitud(self):
        fechas = []
        for requests in self.solicitudes:
            if not self.existe_fecha_solicitud(requests.fecha, fechas):
                fechas.append(requests.fecha)
        return fechas 
    
    def existe_emisor_receptor(self, tipo, lista):
        for x in lista:
            if x == tipo:
                return True
        return False
    
    def obtener_num_emisor(self, fecha): 
        emisores = []
        for requests in self.solicitudes:
            if requests.fecha == fecha:
                if not self.existe_emisor_receptor(requests.nit_emisor, emisores):
                    emisores.append(requests.nit_emisor)
        return str(len(emisores))  
        
    def obtener_num_receptor(self, fecha): 
        receptores = []
        for requests in self.solicitudes:
            if requests.fecha == fecha:
                if not self.existe_emisor_receptor(requests.nit_receptor, receptores):
                    receptores.append(requests.nit_receptor)
        return str(len(receptores)) 
    
    def cantidad_facturas_fecha(self, fecha):
        contador = 0
        for requests in self.solicitudes:
            if requests.fecha == fecha:
                contador += 1
        return contador
    
    def obtener_lista_receptor(self, fecha): 
        receptores = []
        for requests in self.solicitudes:
            if requests.fecha == fecha:
                if self.existe_receptor_iva(requests.nit_receptor, receptores):
                    receptores = self.unir_iva_receptor(requests.nit_receptor, requests.iva, receptores)
                else:
                    receptores.append(requests.get_json_iva_nit_receptor())
        return receptores
    
    def obtener_lista_emisor(self, fecha): 
        emisores = []
        for requests in self.solicitudes:
            if requests.fecha == fecha:
                if self.existe_emisor_iva(requests.nit_emisor, emisores):
                    emisores = self.unir_iva_emisor(requests.nit_emisor, requests.iva, emisores)
                else:
                    emisores.append(requests.get_json_iva_nit_emisor())
        return emisores
    
    def existe_emisor_iva(self, valor, lista):
        for x in lista:
            if x['nit_emisor'] == str(valor):
                return True
        return False
    
    def existe_receptor_iva(self, valor, lista):
        for x in lista:
            if x['nit_receptor'] == valor:
                return True
        return False
    
    def unir_iva_receptor(self, valor_nit, iva_entrada, lista):
        nuevo_iva = 0
        for x in lista:
            if x['nit_receptor'] == valor_nit:
                nuevo_iva = float(x['iva']) + float(iva_entrada)
                nuevo_iva = round(nuevo_iva, 2)
                x['iva'] = nuevo_iva
                return lista
        return lista
    
    def unir_iva_emisor(self, valor_nit, iva_entrada, lista):
        nuevo_iva = 0
        for x in lista:
            if x['nit_emisor'] == valor_nit:
                nuevo_iva = float(x['iva']) + float(iva_entrada)
                nuevo_iva = round(nuevo_iva, 2)
                x['iva'] = nuevo_iva
                return lista
        return lista
    
    def obtener_resumen_iva_rango(self, fecha_1, fecha_2, con_iva): #fecha_1 -> mas baja - fecha_2 -> mas alta
        json_rango = []
        lista_fecha_1 = fecha_1.split('/')
        lista_fecha_2 = fecha_2.split('/')
        for x in self.solicitudes:
            solicitud_dividida = x.fecha.split('/')
            
            if fecha_1 == x.fecha or fecha_2 == x.fecha:
                if con_iva:
                    json_rango.append(x.get_json_iva_nit_rango_total())
                else:
                    json_rango.append(x.get_json_iva_nit_rango_valor())
          
            elif lista_fecha_1[2] < solicitud_dividida[2] and lista_fecha_2[2] > solicitud_dividida[0]: #entre años parametro
                if con_iva:
                    json_rango.append(x.get_json_iva_nit_rango_total())
                else:
                    json_rango.append(x.get_json_iva_nit_rango_valor())
            
            elif lista_fecha_1[2] == solicitud_dividida[2]: #año mas bajo igual
                if lista_fecha_1[1] < solicitud_dividida[1]: #mes lista mayor al del parametro
                    if con_iva:
                        json_rango.append(x.get_json_iva_nit_rango_total())
                    else:
                        json_rango.append(x.get_json_iva_nit_rango_valor()) 
                
                elif lista_fecha_1[1] == solicitud_dividida[1]: #mes mas bajo igual
                    if lista_fecha_1[0] <= solicitud_dividida[0]: #dia mas bajo mayor o igual
                        if con_iva:
                            json_rango.append(x.get_json_iva_nit_rango_total())
                        else:
                            json_rango.append(x.get_json_iva_nit_rango_valor()) 
            
            elif lista_fecha_2[2] == solicitud_dividida[2]: #año mas alto igual
                if lista_fecha_2[1] > solicitud_dividida[1]: #mes lista menor al del parametro
                    if con_iva:
                        json_rango.append(x.get_json_iva_nit_rango_total())
                    else:
                        json_rango.append(x.get_json_iva_nit_rango_valor())
                
                elif lista_fecha_2[1] == solicitud_dividida[1]: #mes mas alto igual
                    if lista_fecha_2[0] >= solicitud_dividida[0]: #dia de la lista menor o igual
                        if con_iva:
                            json_rango.append(x.get_json_iva_nit_rango_total())
                        else:
                            json_rango.append(x.get_json_iva_nit_rango_valor())                         
        return json_rango    
    
    def eliminar_solicitudes(self):
        self.solicitudes.clear()
        self.errores.clear()
            
    #----------------------------------ERROR----------------------------------------------   
    
    def añadir_error(self, fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia):
        nuevo_error = Error(fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia)
        self.errores.append(nuevo_error)
        return True
    
    def modificar_errores_fecha(self, fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia):
        for error in self.errores:
            if error.fecha == fecha:
                error_nit_emisor += int(error.error_nit_emisor)
                error_nit_receptor += int(error.error_nit_receptor)
                error_iva += int(error.error_iva)
                error_total += int(error.error_total)
                error_referencia += int(error.error_referencia)
                error.modificar_error(fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia)
                return
    
    def existe_fecha(self, fecha):
        for error in self.errores:
            if error.fecha == fecha:
                return True
        return False   
    
    def obtener_errores(self):
        json_errores = []
        for error in self.errores:
            json_errores.append(error.get_json())
        return json_errores 
    
    def cantidad_facturas_fecha_error(self, fecha):
        contador = 0
        for error in self.errores:
            if error.fecha == fecha:
                contador += 1
        return contador