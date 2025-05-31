class Barco:
    """
    Representa un barco en el juego.

    Atributos:
        tamaño (int): Número de casillas que ocupa el barco.
        posiciones (list): Lista de tuplas (fila, columna) que ocupa el barco.
    """

    def __init__(self, tamaño):
        """
        Inicializa un barco.

        Args:
            tamaño (int): Número de casillas que ocupa el barco.
        """
        self.tamaño = tamaño
        self.posiciones = []

    def agregar_posicion(self, fila, columna):
        """
        Agrega una posición al barco.

        Args:
            fila (int): Fila de la posición.
            columna (int): Columna de la posición.
        """
        self.posiciones.append((fila, columna))

    def verificar_hundido(self, tablero):
        """
        Verifica si el barco ha sido hundido.

        Args:
            tablero (Tablero): Tablero donde está el barco.

        Returns:
            bool: True si el barco está hundido, False en caso contrario.
        """
        for fila, columna in self.posiciones:
            if tablero.matriz[fila][columna] != 'X':
                return False
        return True
