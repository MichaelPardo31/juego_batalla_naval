from src.btn.tablero import Tablero
from src.btn.barco import Barco

class BatallaNaval:
    def __init__(self, filas, columnas):
        self.tablero = Tablero(filas, columnas)

    def colocar_barcos(self, cantidad):
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

