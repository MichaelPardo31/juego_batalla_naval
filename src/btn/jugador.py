
import hashlib


class Jugador:

    # CONTRASENIA = "agua123"
    CONTRASENIA = "1633be17930e7827733fc093d96922c48b23539c9988e579b99532d318cb9f7e"

    def __init__(self,nombre):
        self.nombre = nombre
        
    
    @classmethod #Se usa en lugar de self cuando el método pertenece a la clase, en lugar de a una instancia de la clase. 
    def autenticar(cls, nombre, contrasenia):
        return contrasenia == cls.CONTRASENIA

# Definir la contraseña fija y calcular su hash SHA-256
# CONTRASENIA = "agua123"
# HASHED_CONTRASENIA = hashlib.sha256(CONTRASENIA.encode()).hexdigest()

