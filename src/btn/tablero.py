class Tablero:
    """
    Representa el tablero del juego.

    Atributos:
        filas (int): Número de filas del tablero.
        columnas (int): Número de columnas del tablero.
        matriz: Matriz que representa el tablero.
    """
    def __init__(self, filas, columnas):
        """
        Inicializa el tablero.

        Args:
            filas (int): Número de filas del tablero.
            columnas (int): Número de columnas del tablero.

        La matriz se inicializa con el carácter "~" para representar agua.
        """
        self.filas = filas
        self.columnas = columnas
        self.matriz = [["~" for _ in range(columnas)] for _ in range(filas)]

    def mostrar(self):

        for fila in self.matriz:
            print(" ".join(fila))

    def colocar_barco(self, fila, columna, tamaño, orientacion) -> bool:
        """
        Representa la colocaciond e un barco.

        Args:
            fila (int): Fila inicial donde se colocará el barco.
            columna (int): Columna inicial donde se colocará el barco.
            tamaño (int): Número de casillas que ocupa el barco.
            orientacion (str): Dirección del barco, "H" para horizontal o "V" para vertical.

        Retorna:
            bool: True si el barco se colocó exitosamente, False si la posición es inválida.
        """
        if tamaño <= 0:
            return False
        if orientacion == "H":
            if columna + tamaño > self.columnas:
                return False
            for i in range(tamaño):
                self.matriz[fila][columna + i] = "B"
        elif orientacion == "V":
            if fila + tamaño > self.filas:
                return False
            for i in range(tamaño):
                self.matriz[fila + i][columna] = "B"
        return True

        