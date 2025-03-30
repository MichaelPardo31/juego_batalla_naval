import hashlib

class Jugador:
    """
    Representa a un jugador en el juego de Batalla Naval.

    Atributos:
        CONTRASENIA (str): Contraseña fija del usuario.
        nombre (str): Nombre del jugador.
    """

    # CONTRASENIA = "agua123"
    CONTRASENIA = "1633be17930e7827733fc093d96922c48b23539c9988e579b99532d318cb9f7e"

    def __init__(self,nombre):
        """
        Representa al jugador.
        """
        self.nombre = nombre
        
    @classmethod
    def autenticar(cls, nombre, contrasenia) -> bool: 
        """
        Verifica si la contraseña ingresada coincide con la almacenada.

        Args:
            nombre (str): Nombre del jugador cualquiera.
            contrasenia (str): Contraseña ingresada por el usuario, tiene que ser igual.

        Retorna:
            bool: True si la contraseña es correcta, False si no.
        """
        return contrasenia == cls.CONTRASENIA

# Definir la contraseña fija y calcular su hash SHA-256
# CONTRASENIA = "agua123"
# HASHED_CONTRASENIA = hashlib.sha256(CONTRASENIA.encode()).hexdigest()

