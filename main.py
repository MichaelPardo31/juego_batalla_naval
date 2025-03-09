from src.btn.jugador import Jugador
from src.btn.batalla_naval import BatallaNaval

def main():
    nombre = input("Ingrese su nombre: ")
    contrasenia = input("Ingrese su contraseña: ")

    if not Jugador.autenticar(nombre, contrasenia):
        print("Acceso denegado.")
        return

    filas = int(input("Ingrese número de filas del tablero: "))
    columnas = int(input("Ingrese número de columnas del tablero: "))
    
    juego = BatallaNaval(filas, columnas)
    juego.tablero.mostrar()

    cantidad_barcos = int(input("¿Cuántos barcos quiere colocar? "))
    juego.colocar_barcos(cantidad_barcos)

if __name__ == "__main__":
    main()
