class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [["~" for _ in range(columnas)] for _ in range(filas)]

    def mostrar(self):
        for fila in self.matriz:
            print(" ".join(fila))

    def colocar_barco(self, fila, columna, tamaño, orientacion):
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

        