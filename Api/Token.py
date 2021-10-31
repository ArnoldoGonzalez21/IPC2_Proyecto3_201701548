class Token():
    
    lexema_valido = ''
    tipo = 0
    LUGAR = 1
    FECHA = 2
    HORA = 3
    
    def __init__(self, lexema, tipo):
        self.lexema_valido = lexema
        self.tipo = tipo