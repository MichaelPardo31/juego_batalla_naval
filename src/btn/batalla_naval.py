from src.btn.tablero import Tablero
from src.btn.barco import Barco

class BatallaNaval:
    """
    gestionando el tablero y la colocación de barcos.

    Atributos:
        tablero (Tablero): Instancia del tablero. 
    """
    def __init__(self, filas, columnas):
        """
        comienza el juego con un tablero introduciendo filas y columnas.

        Args:
            filas (int): Número de filas del tablero.
            columnas (int): Número de columnas del tablero.
        """
        self.tablero = Tablero(filas, columnas)

    def colocar_barcos(self, cantidad):
        """
        Permite poner los barcos en el tablero.

        Args:
            cantidad (int): Número de barcos a colocar.
        """
        for _ in range(cantidad):
            tamaño = int(input("Ingrese el tamaño del barco: "))
            fila = int(input("Fila inicial: "))
            columna = int(input("Columna inicial: "))
            orientacion = input("Ingrese la orientacion de su barco: V/H " ).upper()
            
            barco = Barco(tamaño)
            if not self.tablero.colocar_barco(fila, columna, barco.tamaño, orientacion):
                print("Ubicación inválida. Intente de nuevo.")
                continue

            self.tablero.mostrar()

