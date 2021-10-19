class DTE():
    def __init__(self, codigo_aprobacion, lugar, fecha, hora, referencia, nit_emisor, nit_receptor, valor, iva, total, contador_codigo):
        self.codigo_aprobacion = codigo_aprobacion
        self.lugar = lugar
        self.fecha = fecha
        self.hora = hora
        self.referencia = referencia
        self.nit_emisor = nit_emisor
        self.nit_receptor = nit_receptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.contador_codigo = contador_codigo
        
    def get_json(self):
        return{
            "codigo_aprobacion": self.codigo_aprobacion,
            "lugar": self.lugar,
            "fecha": self.fecha,
            "hora": self.hora,
            "referencia": self.referencia,
            "nit_emisor": self.nit_emisor,
            "nit_receptor": self.nit_receptor,
            "valor": self.valor,
            "iva": self.iva,
            "total": self.total,
            "contador_codigo": self.contador_codigo   
        } 