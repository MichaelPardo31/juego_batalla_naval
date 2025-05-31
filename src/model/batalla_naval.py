from src.model.tablero import Tablero
from src.model.barco import Barco
import random
import time
import os

class BatallaNaval:
    """
    Clase principal que gestiona el juego de Batalla Naval.

    Atributos:
        filas (int): Número de filas del tablero.
        columnas (int): Número de columnas del tablero.
        tablero_jugador (Tablero): Tablero del jugador.
        tablero_computadora (Tablero): Tablero de la computadora.
        barcos_jugador (list): Lista de barcos del jugador.
        barcos_computadora (list): Lista de barcos de la computadora.
        barcos_hundidos_jugador (int): Contador de barcos hundidos del jugador.
        barcos_hundidos_computadora (int): Contador de barcos hundidos de la computadora.
        memoria_computadora (dict): Memoria de disparos de la computadora.
        barcos_jugador_pendientes (int): Contador de barcos del jugador pendientes de colocar.
    """
    def __init__(self, filas, columnas):
        """
        Inicializa el juego con dos tableros.

        Args:
            filas (int): Número de filas del tablero.
            columnas (int): Número de columnas del tablero.
        """
        self.filas = filas
        self.columnas = columnas
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
        self.barcos_jugador_pendientes = 0

    def colocar_barcos_computadora(self, cantidad, tamaño_barco):
        """
        Coloca los barcos de la computadora aleatoriamente.

        Args:
            cantidad (int): Número de barcos a colocar.
            tamaño_barco (int): Tamaño de los barcos a colocar.
        """
        for _ in range(cantidad):
            while True:
                fila = random.randint(0, self.filas - 1)
                columna = random.randint(0, self.columnas - 1)
                orientacion = random.choice(["V", "H"])

                posiciones_a_ocupar = []
                can_place = True
                start_row = fila
                start_col = columna

                if orientacion == "H":
                    if start_col + tamaño_barco > self.columnas:
                        can_place = False
                    else:
                         for i in range(tamaño_barco):
                             posiciones_a_ocupar.append((start_row, start_col + i))
                elif orientacion == "V":
                     if start_row + tamaño_barco > self.filas:
                         can_place = False
                     else:
                         for i in range(tamaño_barco):
                              posiciones_a_ocupar.append((start_row + i, start_col))
                else:
                    can_place = False

                if can_place:
                    for r, c in posiciones_a_ocupar:
                        if self.tablero_computadora.matriz[r][c] != "^":
                            can_place = False
                            break

                if can_place:
                    nuevo_barco = Barco(tamaño_barco)
                    for r, c in posiciones_a_ocupar:
                        self.tablero_computadora.matriz[r][c] = "O"
                        nuevo_barco.agregar_posicion(r, c)

                    self.barcos_computadora.append(nuevo_barco)
                    break

    def colocar_barco_jugador_manual(self, fila, columna, orientacion, tamaño=3):
         """
         Intenta colocar un barco del jugador en una posición específica.
         Utilizado por el backend web.

         Args:
             fila (int): Fila inicial (0-index).
             columna (int): Columna inicial (0-index).
             orientacion (str): 'H' o 'V'.
             tamaño (int): Tamaño del barco (por defecto 3).

         Returns:
             bool: True si se colocó correctamente, False en caso contrario.
         """
         if self.barcos_jugador_pendientes <= 0:
             return False

         posiciones_a_ocupar = []
         can_place = True
         start_row = fila
         start_col = columna

         if orientacion == "H":
             if start_col + tamaño > self.columnas:
                 can_place = False
             else:
                  for i in range(tamaño):
                      posiciones_a_ocupar.append((start_row, start_col + i))
         elif orientacion == "V":
              if start_row + tamaño > self.filas:
                  can_place = False
              else:
                  for i in range(tamaño):
                       posiciones_a_ocupar.append((start_row + i, start_col))
         else:
             can_place = False

         if can_place:
             for r, c in posiciones_a_ocupar:
                 if self.tablero_jugador.matriz[r][c] != "^":
                     can_place = False
                     break

         if can_place:
             nuevo_barco = Barco(tamaño)
             for r, c in posiciones_a_ocupar:
                 self.tablero_jugador.matriz[r][c] = "O"
                 nuevo_barco.agregar_posicion(r, c)

             self.barcos_jugador.append(nuevo_barco)
             self.barcos_jugador_pendientes -= 1
             return True
         else:
             return False

    def disparo_jugador(self, fila, columna):
        """
        Realiza un disparo del jugador en el tablero de la computadora.

        Args:
            fila (int): Fila del disparo (0-index).
            columna (int): Columna del disparo (0-index).

        Returns:
            tuple: (str resultado, bool juego_terminado).
                   resultado: 'agua', 'impacto', 'hundido'.
                   juego_terminado: True si el juego terminó después de este disparo.
        """
        if self.tablero_computadora.matriz[fila][columna] in ['X', '/']:
            return 'ya_disparado', False

        if self.tablero_computadora.matriz[fila][columna] == 'O':
            self.tablero_computadora.matriz[fila][columna] = 'X'
            if self.verificar_barco_hundido(fila, columna, self.tablero_computadora, self.barcos_computadora):
                self.barcos_hundidos_computadora += 1
                if self.verificar_fin_juego():
                    return 'hundido', True
                return 'hundido', False
            else:
                return 'impacto', False
        else:
            self.tablero_computadora.matriz[fila][columna] = '/'
            return 'agua', False

    def disparo_computadora(self):
        """
        Realiza un disparo de la computadora usando estrategia básica.

        Returns:
            tuple: (int fila, int columna, str resultado, bool juego_terminado).
                   fila, columna: Coordenadas del disparo (0-index).
                   resultado: 'agua', 'impacto', 'hundido'.
                   juego_terminado: True si el juego terminó después de este disparo.
        """
        fila, columna = -1, -1

        if self.memoria_computadora['modo_persecucion'] and self.memoria_computadora['casillas_adyacentes']:
            fila, columna = self.memoria_computadora['casillas_adyacentes'].pop(0)
            while (self.tablero_jugador.matriz[fila][columna] in ['X', '/'] and
                   self.memoria_computadora['casillas_adyacentes']):
                 fila, columna = self.memoria_computadora['casillas_adyacentes'].pop(0)

            if self.tablero_jugador.matriz[fila][columna] in ['X', '/']:
                self.memoria_computadora['modo_persecucion'] = False
                self.memoria_computadora['casillas_adyacentes'] = []

        if not self.memoria_computadora['modo_persecucion']:
            while True:
                fila = random.randint(0, self.filas - 1)
                columna = random.randint(0, self.columnas - 1)
                if self.tablero_jugador.matriz[fila][columna] not in ['X', '/']:
                    break

        disparo_resultado = 'agua'
        juego_terminado = False

        if self.tablero_jugador.matriz[fila][columna] == 'O':
            self.tablero_jugador.matriz[fila][columna] = 'X'
            disparo_resultado = 'impacto'

            if self.verificar_barco_hundido(fila, columna, self.tablero_jugador, self.barcos_jugador):
                self.barcos_hundidos_jugador += 1
                disparo_resultado = 'hundido'
                if self.verificar_fin_juego():
                    juego_terminado = True
                self.memoria_computadora['modo_persecucion'] = False
                self.memoria_computadora['casillas_adyacentes'] = []
            else:
                self.memoria_computadora['modo_persecucion'] = True
                self.memoria_computadora['ultimo_acierto'] = (fila, columna)
                if not self.memoria_computadora['casillas_adyacentes']:
                     for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                         new_row, new_col = fila + dr, columna + dc
                         if (0 <= new_row < self.filas and
                             0 <= new_col < self.columnas and
                             self.tablero_jugador.matriz[new_row][new_col] not in ['X', '/']):
                             self.memoria_computadora['casillas_adyacentes'].append((new_row, new_col))

        else:
            self.tablero_jugador.matriz[fila][columna] = '/'
            if not self.memoria_computadora['casillas_adyacentes']:
                 self.memoria_computadora['modo_persecucion'] = False
                 self.memoria_computadora['ultimo_acierto'] = None

        return fila, columna, disparo_resultado, juego_terminado


    def verificar_barco_hundido(self, fila, columna, tablero, barcos):
        """
        Verifica si un barco ha sido hundido después de un disparo en (fila, columna).

        Args:
            fila (int): Fila del disparo (0-index).
            columna (int): Columna del disparo (0-index).
            tablero (Tablero): Tablero a verificar (jugador o computadora).
            barcos (list): Lista de objetos Barco correspondientes al tablero.

        Returns:
            bool: True si el barco que ocupa (fila, columna) está hundido, False en caso contrario.
        """
        impacted_ship = None
        for barco in barcos:
            if (fila, columna) in barco.posiciones:
                impacted_ship = barco
                break

        if impacted_ship:
            for r, c in impacted_ship.posiciones:
                if tablero.matriz[r][c] != 'X':
                    return False
            return True

        return False

    def verificar_fin_juego(self):
        """
        Verifica si el juego ha terminado.

        Returns:
            str: "jugador" si ganó el jugador, "computadora" si ganó la computadora,
                 None si el juego continúa.
        """
        if len(self.barcos_computadora) > 0 and self.barcos_hundidos_computadora == len(self.barcos_computadora) :
            return "jugador"
        elif len(self.barcos_jugador) > 0 and self.barcos_hundidos_jugador == len(self.barcos_jugador) :
            return "computadora"
        return None