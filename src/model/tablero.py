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

        La matriz se inicializa con el carácter "^" para representar agua.
        """
        self.filas = filas
        self.columnas = columnas
        self.matriz = [["^" for _ in range(columnas)] for _ in range(filas)]

    def mostrar(self):
        """
        Muestra el tablero en pantalla.
        """
        # Imprimir números de columna
        print("   ", end="")
        for i in range(self.columnas):
            if i < 9:
                print(f" {i+1} ", end="")
            else:
                print(f"{i+1} ", end="")
        print()

        # Imprimir filas
        for i in range(self.filas):
            if i < 9:
                print(f"{i+1}  ", end="")
            else:
                print(f"{i+1} ", end="")
            
            for j in range(self.columnas):
                print(f" {self.matriz[i][j]} ", end="")
            print()

    def colocar_barco(self, fila, columna, tamaño, orientacion) -> bool:
        """
        Coloca un barco en el tablero.

        Args:
            fila (int): Fila inicial donde se colocará el barco.
            columna (int): Columna inicial donde se colocará el barco.
            tamaño (int): Número de casillas que ocupa el barco.
            orientacion (str): Dirección del barco, "H" para horizontal o "V" para vertical.

        Returns:
            bool: True si el barco se colocó exitosamente, False si la posición es inválida.
        """
        # Verificar que el tamaño del barco sea positivo
        if tamaño <= 0:
            return False

        # Verificar que el barco quepa en el tablero
        if orientacion == "H":
            if columna + tamaño > self.columnas:
                return False
            # Verificar que no haya otros barcos
            for i in range(tamaño):
                if self.matriz[fila][columna + i] != "^":
                    return False
            # Colocar el barco
            for i in range(tamaño):
                self.matriz[fila][columna + i] = "O"
        elif orientacion == "V":
            if fila + tamaño > self.filas:
                return False
            # Verificar que no haya otros barcos
            for i in range(tamaño):
                if self.matriz[fila + i][columna] != "^":
                    return False
            # Colocar el barco
            for i in range(tamaño):
                self.matriz[fila + i][columna] = "O"
        else:
            return False
        return True

    def verificar_posicion(self, fila, columna) -> bool:
        """
        Verifica si una posición es válida para disparar.

        Args:
            fila (int): Fila a verificar.
            columna (int): Columna a verificar.

        Returns:
            bool: True si la posición es válida, False en caso contrario.
        """
        return (0 <= fila < self.filas and 
                0 <= columna < self.columnas and 
                self.matriz[fila][columna] not in ['X', '/'])

    def obtener_estado(self, fila, columna) -> str:
        """
        Obtiene el estado de una casilla.

        Args:
            fila (int): Fila de la casilla.
            columna (int): Columna de la casilla.

        Returns:
            str: Estado de la casilla ("^" para agua, "O" para barco, "X" para impacto, "/" para disparo fallido).
        """
        return self.matriz[fila][columna]

        