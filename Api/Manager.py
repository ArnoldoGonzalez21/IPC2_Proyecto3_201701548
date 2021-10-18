from DTE import DTE

class Manager():
    def __init__(self):
        self.solicitudes = []

    def añadir_solicitud(self, lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total):
        nuevo_dte = DTE(lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total)
        self.solicitudes.append(nuevo_dte)
        return True
    
    def obtener_solicitudes(self):
        json_solicitudes = []
        for requests in self.solicitudes:
            json_solicitudes.append(requests.get_json())
        return json_solicitudes
    
    def existe_referencia(self, referencia):
        for requests in self.solicitudes:
            if requests.referencia == referencia:
                return True
        return False  