from src.btn.tablero import Tablero
from src.btn.barco import Barco
import random
import time
import os

class BatallaNaval:
    """
    Clase principal que gestiona el juego de Batalla Naval.

    Atributos:
        tablero_jugador (Tablero): Tablero del jugador.
        tablero_computadora (Tablero): Tablero de la computadora.
        barcos_jugador (list): Lista de barcos del jugador.
        barcos_computadora (list): Lista de barcos de la computadora.
        barcos_hundidos_jugador (int): Contador de barcos hundidos del jugador.
        barcos_hundidos_computadora (int): Contador de barcos hundidos de la computadora.
        memoria_computadora (dict): Memoria de disparos de la computadora.
    """
    def __init__(self, filas, columnas):
        """
        Inicializa el juego con dos tableros.

        Args:
            filas (int): Número de filas del tablero.
            columnas (int): Número de columnas del tablero.
        """
        self.tablero_jugador = Tablero(filas, columnas)
        self.tablero_computadora = Tablero(filas, columnas)
        self.barcos_jugador = []
        self.barcos_computadora = []
        self.barcos_hundidos_jugador = 0
        self.barcos_hundidos_computadora = 0
        self.memoria_computadora = {
            'ultimo_acierto': None,
            'modo_persecucion': False,
            'direccion': None,
            'casillas_adyacentes': []
        }

    def colocar_barcos_jugador(self, cantidad):
        """
        Permite al jugador colocar sus barcos.

        Args:
            cantidad (int): Número de barcos a colocar.
        """
        for _ in range(cantidad):
            while True:
                fila = int(input("Fila inicial (1-{}): ".format(self.tablero_jugador.filas))) - 1
                columna = int(input("Columna inicial (1-{}): ".format(self.tablero_jugador.columnas))) - 1
                orientacion = input("Orientación (V/H): ").upper()
                
                if not (0 <= fila < self.tablero_jugador.filas and 
                       0 <= columna < self.tablero_jugador.columnas and 
                       orientacion in ['V', 'H']):
                    print("Valores inválidos. Intente de nuevo.")
                    continue

                barco = Barco(3)  # Todos los barcos son de tamaño 3
                if self.tablero_jugador.colocar_barco(fila, columna, barco.tamaño, orientacion):
                    self.barcos_jugador.append(barco)
                    self.tablero_jugador.mostrar()
                    break
                else:
                    print("Posición inválida. Intente de nuevo.")

    def colocar_barcos_computadora(self, cantidad):
        """
        Coloca los barcos de la computadora aleatoriamente.

        Args:
            cantidad (int): Número de barcos a colocar.
        """
        for _ in range(cantidad):
            while True:
                fila = random.randint(0, self.tablero_computadora.filas - 1)
                columna = random.randint(0, self.tablero_computadora.columnas - 1)
                orientacion = random.choice(['V', 'H'])
                
                barco = Barco(3)  # Todos los barcos son de tamaño 3
                if self.tablero_computadora.colocar_barco(fila, columna, barco.tamaño, orientacion):
                    self.barcos_computadora.append(barco)
                    break

    def disparo_jugador(self, fila, columna):
        """
        Realiza un disparo del jugador.

        Args:
            fila (int): Fila del disparo.
            columna (int): Columna del disparo.

        Returns:
            bool: True si el disparo fue exitoso, False si ya se había disparado ahí.
        """
        if self.tablero_computadora.matriz[fila][columna] in ['X', '/']:
            return False

        if self.tablero_computadora.matriz[fila][columna] == 'B':
            self.tablero_computadora.matriz[fila][columna] = 'X'
            if self.verificar_barco_hundido(fila, columna, self.tablero_computadora, self.barcos_computadora):
                self.barcos_hundidos_computadora += 1
                print("¡Has hundido un barco!")
            else:
                print("¡Le has dado a un barco!")
        else:
            self.tablero_computadora.matriz[fila][columna] = '/'
            print("¡Disparo al agua!")
        return True

    def disparo_computadora(self):
        """
        Realiza un disparo de la computadora usando estrategia básica.

        Returns:
            tuple: (fila, columna) del disparo realizado.
        """
        if self.memoria_computadora['modo_persecucion']:
            # Modo persecución: buscar alrededor del último acierto
            fila, columna = self.memoria_computadora['casillas_adyacentes'].pop(0)
        else:
            # Modo búsqueda: disparo aleatorio
            while True:
                fila = random.randint(0, self.tablero_jugador.filas - 1)
                columna = random.randint(0, self.tablero_jugador.columnas - 1)
                if self.tablero_jugador.matriz[fila][columna] not in ['X', '/']:
                    break

        if self.tablero_jugador.matriz[fila][columna] == 'B':
            self.tablero_jugador.matriz[fila][columna] = 'X'
            if self.verificar_barco_hundido(fila, columna, self.tablero_jugador, self.barcos_jugador):
                self.barcos_hundidos_jugador += 1
                print("¡La computadora ha hundido uno de tus barcos!")
                self.memoria_computadora['modo_persecucion'] = False
            else:
                print("¡La computadora ha dado en uno de tus barcos!")
                # Activar modo persecución
                self.memoria_computadora['modo_persecucion'] = True
                self.memoria_computadora['ultimo_acierto'] = (fila, columna)
                # Agregar casillas adyacentes
                for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                    new_fila, new_col = fila + dr, columna + dc
                    if (0 <= new_fila < self.tablero_jugador.filas and 
                        0 <= new_col < self.tablero_jugador.columnas and 
                        self.tablero_jugador.matriz[new_fila][new_col] not in ['X', '/']):
                        self.memoria_computadora['casillas_adyacentes'].append((new_fila, new_col))
        else:
            self.tablero_jugador.matriz[fila][columna] = '/'
            print("La computadora ha disparado al agua.")
            self.memoria_computadora['modo_persecucion'] = False

        return fila, columna

    def verificar_barco_hundido(self, fila, columna, tablero, barcos):
        """
        Verifica si un barco ha sido hundido.

        Args:
            fila (int): Fila del disparo.
            columna (int): Columna del disparo.
            tablero (Tablero): Tablero a verificar.
            barcos (list): Lista de barcos.

        Returns:
            bool: True si el barco está hundido, False en caso contrario.
        """
        # Buscar el barco que contiene la casilla
        for barco in barcos:
            if barco.verificar_hundido(tablero):
                return True
        return False

    def verificar_fin_juego(self):
        """
        Verifica si el juego ha terminado.

        Returns:
            str: "jugador" si ganó el jugador, "computadora" si ganó la computadora,
                 None si el juego continúa.
        """
        if self.barcos_hundidos_computadora == len(self.barcos_computadora):
            return "jugador"
        elif self.barcos_hundidos_jugador == len(self.barcos_jugador):
            return "computadora"
        return None

