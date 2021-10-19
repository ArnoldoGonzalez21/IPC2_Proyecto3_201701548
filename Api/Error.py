class Error():
    def __init__(self, fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia):
        self.fecha = fecha
        self.error_nit_emisor = error_nit_emisor
        self.error_nit_receptor = error_nit_receptor
        self.error_iva = error_iva
        self.error_total = error_total
        self.error_referencia = error_referencia
    
    def modificar_error(self, fecha, error_nit_emisor, error_nit_receptor, error_iva, error_total, error_referencia):
        self.fecha = fecha
        self.error_nit_emisor = error_nit_emisor
        self.error_nit_receptor = error_nit_receptor
        self.error_iva = error_iva
        self.error_total = error_total
        self.error_referencia = error_referencia
    
    def get_json(self):
        return{
            "fecha": self.fecha,
            "error_nit_emisor": self.error_nit_emisor,
            "error_nit_receptor": self.error_nit_receptor,
            "error_iva": self.error_iva,
            "error_total": self.error_total,
            "error_referencia": self.error_referencia
        }    