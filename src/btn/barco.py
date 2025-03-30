class Barco:
    """
    Representa un barco en el juego

    Atributos:
        tamaño (int): La cantidad de casillas que ocupa el barco en el tablero.
    """

    def __init__(self, tamaño):
        """
        Inicializa un barco con un tamaño específico.

        Args:
            tamaño (int): La cantidad de casillas que ocupa el barco.
        """
        self.tamaño = tamaño
