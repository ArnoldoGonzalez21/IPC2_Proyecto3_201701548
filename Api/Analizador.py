from Token import Token

class Analizador():
    
    lexema = ''
    estado = 0
    tokens = []
    tipos = Token("lexema", -1)
    
    def agregar_token(self, tipo):
        nuevo_token = Token(self.lexema, tipo)
        self.tokens.append(nuevo_token)
        self.lexema = ''
        self.estado = 0
            
    def analizador_estados(self, entrada):
        self.estado = 0
        self.lexema = ''
        self.tokens = []
        entrada += '`'
        actual = ''
        longitud = len(entrada)
        for contador in range(longitud):
            actual = entrada[contador]
            if self.estado == 0:
                if actual.isalpha():
                    self.estado = 1
                    self.lexema += actual
                     
                elif actual.isdigit():
                    self.estado = 2
                    self.lexema += actual
                
                elif actual == ' ':
                    self.estado = 0
                    
                elif actual == '`' and contador == longitud - 1:
                    print('Análisis terminado')
            
            elif self.estado == 1:
                if actual.isalpha():
                    self.estado = 1
                    self.lexema += actual
                if actual == ',':
                    self.agregar_token(self.tipos.LUGAR)
                        
            elif self.estado == 2:
                if actual.isdigit():
                    self.estado = 2
                    self.lexema += actual
                elif actual == '/':
                    self.estado = 3
                    self.lexema += actual    
                elif actual == ':':
                    self.estado = 5
                    self.lexema += actual 
                    
            elif self.estado == 3:
                if actual.isdigit():
                    self.estado = 3
                    self.lexema += actual
                elif actual == '/':
                    self.estado = 4
                    self.lexema += actual                          
                                
            elif self.estado == 4:
                if actual.isdigit():
                    self.estado = 4
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.FECHA)  
            
            elif self.estado == 5:
                if actual.isdigit():
                    self.estado = 5
                    self.lexema += actual
                elif actual == ' ' or actual.isalpha():
                    self.estado = 6
                    self.lexema += actual        
            
            elif self.estado == 6:
                if actual.isalpha():
                    self.estado = 6
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.HORA)  
            
    def reiniciar_tokens(self):
        self.tokens.clear()
        
    def obtener_tokens(self):
        tiempo = {'lugar': '', 'fecha': '', 'hora': ''}
        for x in self.tokens:
            if x.tipo == 1:
                tiempo['lugar'] = x.lexema_valido
            elif x.tipo == 2:
                tiempo['fecha'] = x.lexema_valido
            elif x.tipo == 3:
                tiempo['hora'] = x.lexema_valido
        return tiempo
    