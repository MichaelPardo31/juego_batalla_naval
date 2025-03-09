class Jugador:

    CONTRASENIA = "agua123"

    def __init__(self,nombre):
        self.nombre = nombre
        
    
    @classmethod
    def autenticar(cls, nombre, contrasenia):
        return contrasenia == cls.CONTRASENIA